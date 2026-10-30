CREATE OR REPLACE FUNCTION public.fn_seed_role(p_id uuid, p_name text)
RETURNS void LANGUAGE plpgsql AS $function$
BEGIN
    INSERT INTO roles (id, name, is_active)
    VALUES (p_id, p_name, true)
    ON CONFLICT (name) DO NOTHING;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_seed_user(
    p_id uuid, p_email text, p_full_name text, p_password_hash text, p_role_name text
) RETURNS uuid LANGUAGE plpgsql AS $function$
DECLARE v_role_id uuid; v_user_id uuid;
BEGIN
    SELECT id INTO v_role_id FROM roles WHERE name = p_role_name;
    IF v_role_id IS NULL THEN
        RAISE EXCEPTION 'Unknown seeded role: %', p_role_name;
    END IF;
    INSERT INTO users (id, email, full_name, password_hash, role_id, is_active)
    VALUES (p_id, p_email, p_full_name, p_password_hash, v_role_id, true)
    ON CONFLICT (email) DO NOTHING;
    SELECT id INTO v_user_id FROM users WHERE email = p_email;
    RETURN v_user_id;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_seed_student_profile(p_user_id uuid, p_student_code text)
RETURNS void LANGUAGE plpgsql AS $function$
BEGIN
    INSERT INTO student_profiles (
        user_id, student_code, faculty, cohort, phone, address,
        emergency_contact_name, emergency_contact_phone
    ) VALUES (p_user_id, p_student_code, '', '', '', '', '', '')
    ON CONFLICT (user_id) DO NOTHING;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_seed_utility(
    p_id uuid, p_code text, p_name text, p_unit text, p_rounding_scale integer
) RETURNS void LANGUAGE plpgsql AS $function$
BEGIN
    INSERT INTO utilities (id, code, name, unit, rounding_scale, is_active)
    VALUES (p_id, p_code, p_name, p_unit, p_rounding_scale, true)
    ON CONFLICT (code) DO NOTHING;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_db_ready()
RETURNS integer LANGUAGE sql STABLE AS $function$
    SELECT 1;
$function$;
