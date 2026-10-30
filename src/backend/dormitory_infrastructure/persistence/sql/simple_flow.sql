CREATE OR REPLACE FUNCTION public.fn_create_simple_room(
    p_id uuid, p_building_id uuid, p_code text, p_floor integer,
    p_capacity integer, p_monthly_rate numeric
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE
    v_building buildings%ROWTYPE;
    v_utility record;
BEGIN
    SELECT * INTO v_building FROM buildings WHERE id = p_building_id AND is_active FOR UPDATE;
    IF NOT FOUND THEN RETURN 'BUILDING_NOT_FOUND'; END IF;
    IF p_floor < 1 OR p_floor > v_building.floors OR p_capacity < 1
       OR p_capacity > 12 OR p_monthly_rate < 0 THEN RETURN 'INVALID_ROOM'; END IF;
    INSERT INTO rooms (id, building_id, code, floor, capacity, monthly_rate,
                       gender_policy, status, is_active)
    VALUES (p_id, p_building_id, upper(trim(p_code)), p_floor, p_capacity,
            p_monthly_rate, 'Mixed', 'Available', true);
    INSERT INTO beds (id, room_id, code, is_active)
    SELECT gen_random_uuid(), p_id, 'G' || n, true
    FROM generate_series(1, p_capacity) AS n;
    FOR v_utility IN SELECT id, code FROM utilities WHERE upper(code) IN ('ELECTRICITY', 'WATER') LOOP
        INSERT INTO meters (id, utility_id, room_id, meter_code, initial_reading, is_active)
        VALUES (gen_random_uuid(), v_utility.id, p_id,
                upper(v_utility.code) || '-' || replace(p_id::text, '-', ''), 0, true);
    END LOOP;
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_rooms(p_building_id uuid DEFAULT NULL, p_staff_id uuid DEFAULT NULL)
RETURNS TABLE (
    id uuid, building_id uuid, building_code text,
    code text, floor integer, gender_policy text,
    managed_by_staff_id uuid, status text, is_active boolean, note text,
    capacity integer, monthly_rate numeric
) LANGUAGE sql STABLE AS $function$
    SELECT r.id, r.building_id, b.code::text,
           r.code::text, r.floor, r.gender_policy::text,
           r.managed_by_staff_id, r.status::text, r.is_active, r.note::text,
           r.capacity, r.monthly_rate
    FROM rooms AS r
    JOIN buildings AS b ON b.id = r.building_id
    WHERE (p_building_id IS NULL OR r.building_id = p_building_id)
      AND (p_staff_id IS NULL OR r.managed_by_staff_id = p_staff_id)
    ORDER BY r.floor, r.code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_room(p_id uuid)
RETURNS TABLE (
    id uuid, building_id uuid, building_code text,
    code text, floor integer, gender_policy text,
    managed_by_staff_id uuid, status text, is_active boolean, note text,
    capacity integer, monthly_rate numeric
) LANGUAGE sql STABLE AS $function$
    SELECT * FROM public.fn_list_rooms(NULL, NULL) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_create_application(
    p_id uuid, p_student_id uuid, p_term_code text, p_room_id uuid
) RETURNS text LANGUAGE plpgsql AS $function$
BEGIN
    PERFORM pg_advisory_xact_lock(hashtextextended(p_student_id::text, 0));
    PERFORM 1 FROM rooms
    WHERE id = p_room_id AND is_active AND status = 'Available';
    IF NOT FOUND THEN RETURN 'ROOM_NOT_FOUND'; END IF;
    IF EXISTS (SELECT 1 FROM housing_applications
               WHERE student_id = p_student_id AND term_code = upper(trim(p_term_code))
                 AND status IN ('Submitted', 'Approved')) THEN
        RETURN 'APPLICATION_ALREADY_EXISTS';
    END IF;
    IF EXISTS (SELECT 1 FROM contracts WHERE student_id = p_student_id AND status = 'Active') THEN
        RETURN 'STUDENT_ALREADY_HOUSED';
    END IF;
    INSERT INTO housing_applications
        (id, student_id, term_code, requested_room_id, status)
    VALUES (p_id, p_student_id, upper(trim(p_term_code)), p_room_id, 'Submitted');
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_applications(
    p_user_id uuid, p_role text, p_status text DEFAULT NULL
) RETURNS TABLE (
    id uuid, student_id uuid, student_name text, term_code text,
    status text, rejection_reason text, created_at timestamptz,
    room_id uuid, room_code text
) LANGUAGE sql STABLE AS $function$
    SELECT a.id, a.student_id, u.full_name::text, a.term_code::text,
           a.status::text, a.rejection_reason::text, a.created_at,
           a.requested_room_id, r.code::text
    FROM housing_applications AS a
    JOIN users AS u ON u.id = a.student_id
    LEFT JOIN rooms AS r ON r.id = a.requested_room_id
    WHERE (p_role <> 'Student' OR a.student_id = p_user_id)
      AND (p_status IS NULL OR a.status = p_status)
    ORDER BY a.created_at DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_application(p_id uuid)
RETURNS TABLE (
    id uuid, student_id uuid, student_name text, term_code text,
    status text, rejection_reason text, created_at timestamptz,
    room_id uuid, room_code text
) LANGUAGE sql STABLE AS $function$
    SELECT * FROM public.fn_list_applications(NULL, 'Admin', NULL) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_assign_room(
    p_application_id uuid, p_contract_id uuid, p_assignment_id uuid,
    p_contract_no text, p_start_date date, p_end_date date
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE
    v_application housing_applications%ROWTYPE;
    v_room rooms%ROWTYPE;
    v_bed_id uuid;
    v_rate numeric;
BEGIN
    SELECT * INTO v_application FROM housing_applications
    WHERE id = p_application_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'APPLICATION_NOT_FOUND'; END IF;
    IF v_application.status <> 'Approved' THEN RETURN 'APPLICATION_NOT_APPROVED'; END IF;
    IF v_application.requested_room_id IS NULL THEN RETURN 'ROOM_NOT_FOUND'; END IF;
    IF EXISTS (SELECT 1 FROM contracts WHERE application_id = p_application_id) THEN
        RETURN 'CONTRACT_ALREADY_EXISTS';
    END IF;
    IF EXISTS (SELECT 1 FROM contracts WHERE student_id = v_application.student_id
               AND status = 'Active' AND start_date <= p_end_date AND end_date >= p_start_date) THEN
        RETURN 'STUDENT_ALREADY_HOUSED';
    END IF;
    SELECT * INTO v_room FROM rooms WHERE id = v_application.requested_room_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'ROOM_NOT_FOUND'; END IF;
    IF NOT v_room.is_active OR v_room.status <> 'Available' THEN RETURN 'ROOM_NOT_AVAILABLE'; END IF;
    SELECT bed.id INTO v_bed_id FROM beds AS bed
    WHERE bed.room_id = v_room.id AND bed.is_active
      AND NOT EXISTS (SELECT 1 FROM bed_assignments AS ba
                      JOIN contracts AS occupied ON occupied.id = ba.contract_id
                      WHERE ba.bed_id = bed.id AND ba.start_date <= p_end_date
                        AND COALESCE(ba.end_date, occupied.end_date) >= p_start_date)
    ORDER BY bed.code LIMIT 1 FOR UPDATE OF bed;
    IF v_bed_id IS NULL THEN RETURN 'ROOM_FULL'; END IF;
    v_rate := v_room.monthly_rate;
    INSERT INTO contracts (id, contract_no, student_id, application_id,
                           start_date, end_date, status, base_rate)
    VALUES (p_contract_id, p_contract_no, v_application.student_id, p_application_id,
            p_start_date, p_end_date, 'Active', v_rate);
    INSERT INTO bed_assignments (id, contract_id, bed_id, start_date, status)
    VALUES (p_assignment_id, p_contract_id, v_bed_id, p_start_date, 'Active');
    RETURN 'OK';
END;
$function$;
