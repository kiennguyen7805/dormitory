-- Frozen for migration 0018; keep independent of later schema changes.
CREATE OR REPLACE FUNCTION public.fn_list_applications(
    p_user_id uuid, p_role text, p_status text DEFAULT NULL
)
RETURNS TABLE (
    id uuid, student_id uuid, student_name text, term_code text,
    preferred_room_type_id uuid, preferred_room_type_name text,
    status text, rejection_reason text, created_at timestamptz
)
LANGUAGE sql STABLE
AS $function$
    SELECT a.id, a.student_id, u.full_name::text, a.term_code::text,
           a.preferred_room_type_id, rt.name::text, a.status::text,
           a.rejection_reason::text, a.created_at
    FROM housing_applications AS a
    JOIN users AS u ON u.id = a.student_id
    JOIN room_types AS rt ON rt.id = a.preferred_room_type_id
    WHERE (p_role <> 'Student' OR a.student_id = p_user_id)
      AND (p_status IS NULL OR a.status = p_status)
    ORDER BY a.created_at DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_application(p_id uuid)
RETURNS TABLE (
    id uuid, student_id uuid, student_name text, term_code text,
    preferred_room_type_id uuid, preferred_room_type_name text,
    status text, rejection_reason text, created_at timestamptz
)
LANGUAGE sql STABLE
AS $function$
    SELECT a.id, a.student_id, u.full_name::text, a.term_code::text,
           a.preferred_room_type_id, rt.name::text, a.status::text,
           a.rejection_reason::text, a.created_at
    FROM housing_applications AS a
    JOIN users AS u ON u.id = a.student_id
    JOIN room_types AS rt ON rt.id = a.preferred_room_type_id
    WHERE a.id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_contracts(p_user_id uuid, p_role text)
RETURNS TABLE (
    id uuid, contract_no text, student_id uuid, student_name text,
    application_id uuid, start_date date, end_date date, status text,
    base_rate numeric, assignment_id uuid, bed_id uuid,
    building_code text, room_code text, bed_code text,
    assignment_start_date date, assignment_end_date date, assignment_status text
)
LANGUAGE sql STABLE
AS $function$
    SELECT c.id, c.contract_no::text, c.student_id, u.full_name::text,
           c.application_id, c.start_date, c.end_date, c.status::text,
           c.base_rate, a.id, a.bed_id, b.code::text, r.code::text,
           bed.code::text, a.start_date, a.end_date, a.status::text
    FROM contracts AS c
    JOIN users AS u ON u.id = c.student_id
    LEFT JOIN LATERAL (
        SELECT * FROM bed_assignments
        WHERE contract_id = c.id AND status = 'Active'
        ORDER BY start_date DESC LIMIT 1
    ) AS a ON true
    LEFT JOIN beds AS bed ON bed.id = a.bed_id
    LEFT JOIN rooms AS r ON r.id = bed.room_id
    LEFT JOIN buildings AS b ON b.id = r.building_id
    WHERE p_role <> 'Student' OR c.student_id = p_user_id
    ORDER BY c.start_date DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_contract(p_id uuid)
RETURNS TABLE (
    id uuid, contract_no text, student_id uuid, student_name text,
    application_id uuid, start_date date, end_date date, status text,
    base_rate numeric, assignment_id uuid, bed_id uuid,
    building_code text, room_code text, bed_code text,
    assignment_start_date date, assignment_end_date date, assignment_status text
)
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM public.fn_list_contracts(NULL, 'Admin') WHERE id = p_id;
$function$;
