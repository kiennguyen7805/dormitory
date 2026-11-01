-- Frozen for migration 0019; keep independent of later schema changes.
CREATE OR REPLACE FUNCTION public.fn_create_application(
    p_id uuid, p_student_id uuid, p_term_code text, p_room_type_id uuid
)
RETURNS text
LANGUAGE plpgsql
AS $function$
BEGIN
    PERFORM pg_advisory_xact_lock(hashtextextended(p_student_id::text, 0));
    IF EXISTS (
        SELECT 1 FROM housing_applications
        WHERE student_id = p_student_id
          AND term_code = upper(trim(p_term_code))
          AND status IN ('Submitted', 'Approved')
    ) THEN RETURN 'APPLICATION_ALREADY_EXISTS'; END IF;
    INSERT INTO housing_applications (
        id, student_id, term_code, preferred_room_type_id, status
    ) VALUES (
        p_id, p_student_id, upper(trim(p_term_code)), p_room_type_id, 'Submitted'
    );
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_review_application(
    p_application_id uuid, p_reviewer_id uuid, p_status text, p_reason text
)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    v_status text;
BEGIN
    SELECT status INTO v_status FROM housing_applications
    WHERE id = p_application_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'NOT_FOUND'; END IF;
    IF v_status <> 'Submitted' THEN RETURN 'APPLICATION_INVALID_STATE'; END IF;
    IF p_status = 'Rejected' AND (p_reason IS NULL OR trim(p_reason) = '') THEN
        RETURN 'REJECTION_REASON_REQUIRED';
    END IF;
    UPDATE housing_applications SET
        status = p_status, rejection_reason = p_reason,
        reviewed_by_user_id = p_reviewer_id, reviewed_at = CURRENT_TIMESTAMP
    WHERE id = p_application_id;
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_check_bed_available(
    p_bed_id uuid, p_start_date date, p_end_date date
)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    v_bed_active boolean;
    v_room_active boolean;
BEGIN
    SELECT bed.is_active, room.is_active INTO v_bed_active, v_room_active
    FROM beds AS bed
    JOIN rooms AS room ON room.id = bed.room_id
    WHERE bed.id = p_bed_id
    FOR UPDATE OF bed;
    IF NOT FOUND THEN RETURN 'BED_NOT_FOUND'; END IF;
    IF NOT v_bed_active OR NOT v_room_active THEN RETURN 'BED_NOT_AVAILABLE'; END IF;
    IF EXISTS (
        SELECT 1 FROM bed_assignments
        WHERE bed_id = p_bed_id AND start_date <= p_end_date
          AND (end_date IS NULL OR end_date >= p_start_date)
    ) THEN RETURN 'BED_ASSIGNMENT_CONFLICT'; END IF;
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_assign_bed(
    p_application_id uuid, p_contract_id uuid, p_assignment_id uuid,
    p_contract_no text, p_bed_id uuid, p_start_date date, p_end_date date
)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    v_student_id uuid;
    v_status text;
    v_bed_status text;
    v_base_rate numeric;
BEGIN
    SELECT student_id, status INTO v_student_id, v_status
    FROM housing_applications WHERE id = p_application_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'APPLICATION_NOT_FOUND'; END IF;
    IF v_status <> 'Approved' THEN RETURN 'APPLICATION_NOT_APPROVED'; END IF;
    IF EXISTS (SELECT 1 FROM contracts WHERE application_id = p_application_id) THEN
        RETURN 'CONTRACT_ALREADY_EXISTS';
    END IF;
    v_bed_status := public.fn_check_bed_available(p_bed_id, p_start_date, p_end_date);
    IF v_bed_status <> 'OK' THEN RETURN v_bed_status; END IF;
    SELECT rt.default_monthly_rate INTO v_base_rate
    FROM beds AS bed
    JOIN rooms AS room ON room.id = bed.room_id
    JOIN room_types AS rt ON rt.id = room.room_type_id
    WHERE bed.id = p_bed_id;
    INSERT INTO contracts (
        id, contract_no, student_id, application_id, start_date,
        end_date, status, base_rate
    ) VALUES (
        p_contract_id, p_contract_no, v_student_id, p_application_id,
        p_start_date, p_end_date, 'Active', v_base_rate
    );
    INSERT INTO bed_assignments (id, contract_id, bed_id, start_date, status)
    VALUES (p_assignment_id, p_contract_id, p_bed_id, p_start_date, 'Active');
    RETURN 'OK';
END;
$function$;


-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_terminate_contract(
    p_contract_id uuid, p_termination_date date
)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    v_contract_status text;
    v_contract_end date;
    v_assignment_id uuid;
    v_assignment_start date;
BEGIN
    SELECT status, end_date INTO v_contract_status, v_contract_end
    FROM contracts WHERE id = p_contract_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'CONTRACT_NOT_FOUND'; END IF;
    IF v_contract_status <> 'Active' THEN RETURN 'CONTRACT_NOT_ACTIVE'; END IF;
    SELECT id, start_date INTO v_assignment_id, v_assignment_start
    FROM bed_assignments
    WHERE contract_id = p_contract_id AND status = 'Active' FOR UPDATE;
    IF NOT FOUND THEN RETURN 'ACTIVE_ASSIGNMENT_NOT_FOUND'; END IF;
    IF p_termination_date < v_assignment_start OR p_termination_date > v_contract_end THEN
        RETURN 'TERMINATION_DATE_INVALID';
    END IF;
    UPDATE bed_assignments SET status = 'Ended', end_date = p_termination_date
    WHERE id = v_assignment_id;
    UPDATE contracts SET status = 'Terminated', terminated_at = CURRENT_TIMESTAMP,
                         updated_at = CURRENT_TIMESTAMP
    WHERE id = p_contract_id;
    RETURN 'OK';
END;
$function$;
