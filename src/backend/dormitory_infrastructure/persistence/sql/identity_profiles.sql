CREATE OR REPLACE FUNCTION public.fn_get_student_profile(p_user_id uuid)
RETURNS TABLE (
    user_id uuid,
    email text,
    full_name text,
    student_code text,
    faculty text,
    cohort text,
    date_of_birth date,
    gender text,
    phone text,
    address text,
    identity_number text,
    emergency_contact_name text,
    emergency_contact_phone text
)
LANGUAGE sql
STABLE
AS $function$
    SELECT sp.user_id, u.email::text, u.full_name::text,
           sp.student_code::text, sp.faculty::text, sp.cohort::text,
           sp.date_of_birth, sp.gender::text, sp.phone::text,
           sp.address::text, sp.identity_number::text,
           sp.emergency_contact_name::text, sp.emergency_contact_phone::text
    FROM student_profiles AS sp
    JOIN users AS u ON u.id = sp.user_id
    WHERE sp.user_id = p_user_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_upsert_student_profile(
    p_user_id uuid,
    p_student_code text,
    p_faculty text,
    p_cohort text,
    p_date_of_birth date,
    p_gender text,
    p_phone text,
    p_address text,
    p_identity_number text,
    p_emergency_contact_name text,
    p_emergency_contact_phone text
)
RETURNS void
LANGUAGE sql
AS $function$
    INSERT INTO student_profiles (
        user_id, student_code, faculty, cohort, date_of_birth, gender,
        phone, address, identity_number, emergency_contact_name,
        emergency_contact_phone
    ) VALUES (
        p_user_id, p_student_code, p_faculty, p_cohort, p_date_of_birth,
        p_gender, p_phone, p_address, p_identity_number,
        p_emergency_contact_name, p_emergency_contact_phone
    )
    ON CONFLICT (user_id) DO UPDATE SET
        student_code = EXCLUDED.student_code,
        faculty = EXCLUDED.faculty,
        cohort = EXCLUDED.cohort,
        date_of_birth = EXCLUDED.date_of_birth,
        gender = EXCLUDED.gender,
        phone = EXCLUDED.phone,
        address = EXCLUDED.address,
        identity_number = EXCLUDED.identity_number,
        emergency_contact_name = EXCLUDED.emergency_contact_name,
        emergency_contact_phone = EXCLUDED.emergency_contact_phone,
        updated_at = CURRENT_TIMESTAMP;
$function$;
