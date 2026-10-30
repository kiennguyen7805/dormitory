CREATE OR REPLACE FUNCTION public.fn_auth_user(
    p_user_id uuid DEFAULT NULL,
    p_email text DEFAULT NULL,
    p_refresh_hash text DEFAULT NULL
)
RETURNS TABLE (
    user_id uuid,
    email text,
    full_name text,
    password_hash text,
    is_active boolean,
    role_name text,
    refresh_token_expires_at timestamptz,
    refresh_token_revoked_at timestamptz
)
LANGUAGE sql
STABLE
AS $function$
    SELECT
        u.id,
        u.email::text,
        u.full_name::text,
        u.password_hash::text,
        u.is_active,
        r.name::text,
        u.refresh_token_expires_at,
        u.refresh_token_revoked_at
    FROM users AS u
    JOIN roles AS r ON r.id = u.role_id
    WHERE (p_user_id IS NOT NULL AND u.id = p_user_id)
       OR (p_email IS NOT NULL AND u.email = p_email)
       OR (p_refresh_hash IS NOT NULL AND u.refresh_token_hash = p_refresh_hash);
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_register_student(
    p_user_id uuid,
    p_email text,
    p_full_name text,
    p_password_hash text,
    p_student_code text,
    p_date_of_birth date
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
DECLARE
    v_role_id uuid;
BEGIN
    SELECT id INTO v_role_id FROM roles WHERE name = 'Student';
    IF v_role_id IS NULL THEN
        RETURN false;
    END IF;
    INSERT INTO users (id, email, full_name, password_hash, role_id, is_active)
    VALUES (p_user_id, p_email, p_full_name, p_password_hash, v_role_id, true);
    INSERT INTO student_profiles (
        user_id, student_code, faculty, cohort, phone, address,
        emergency_contact_name, emergency_contact_phone, date_of_birth
    ) VALUES (
        p_user_id, p_student_code, '', '', '', '', '', '', p_date_of_birth
    );
    RETURN true;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_set_refresh_token(
    p_user_id uuid,
    p_token_hash text,
    p_expires_at timestamptz
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
BEGIN
    UPDATE users
    SET refresh_token_hash = p_token_hash,
        refresh_token_expires_at = p_expires_at,
        refresh_token_revoked_at = NULL
    WHERE id = p_user_id;
    RETURN FOUND;
END;
$function$;
