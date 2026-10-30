CREATE OR REPLACE FUNCTION public.fn_count_students()
RETURNS bigint
LANGUAGE sql
STABLE
AS $function$
    SELECT count(*) FROM student_profiles;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_students(p_limit integer, p_offset integer)
RETURNS TABLE (
    user_id uuid,
    student_code text,
    full_name text,
    date_of_birth date,
    email text,
    is_active boolean
)
LANGUAGE sql
STABLE
AS $function$
    SELECT sp.user_id, sp.student_code::text, u.full_name::text,
           sp.date_of_birth, u.email::text, u.is_active
    FROM student_profiles AS sp
    JOIN users AS u ON u.id = sp.user_id
    ORDER BY u.full_name, sp.student_code
    LIMIT p_limit OFFSET p_offset;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_student(p_user_id uuid)
RETURNS TABLE (
    user_id uuid,
    student_code text,
    full_name text,
    date_of_birth date,
    email text,
    is_active boolean
)
LANGUAGE sql
STABLE
AS $function$
    SELECT sp.user_id, sp.student_code::text, u.full_name::text,
           sp.date_of_birth, u.email::text, u.is_active
    FROM student_profiles AS sp
    JOIN users AS u ON u.id = sp.user_id
    WHERE sp.user_id = p_user_id;
$function$;
