-- Each statement is installed separately by Alembic.
CREATE OR REPLACE FUNCTION public.fn_get_user(p_user_id uuid)
RETURNS TABLE (
    user_id uuid,
    email text,
    full_name text,
    role_name text,
    is_active boolean
)
LANGUAGE sql
STABLE
AS $function$
    SELECT users.user_id, users.email, users.full_name, users.role_name,
           users.is_active
    FROM public.fn_list_users(NULL) AS users
    WHERE users.user_id = p_user_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_create_user(
    p_user_id uuid,
    p_email text,
    p_full_name text,
    p_password_hash text,
    p_role_name text
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
DECLARE
    v_role_id uuid;
BEGIN
    SELECT id INTO v_role_id FROM roles WHERE name = p_role_name;
    IF v_role_id IS NULL THEN
        RETURN false;
    END IF;
    INSERT INTO users (id, email, full_name, password_hash, role_id, is_active)
    VALUES (p_user_id, p_email, p_full_name, p_password_hash, v_role_id, true);
    RETURN true;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_update_user(
    p_user_id uuid,
    p_full_name text,
    p_role_name text,
    p_is_active boolean,
    p_actor_id uuid
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
DECLARE
    v_role_id uuid;
BEGIN
    SELECT id INTO v_role_id FROM roles WHERE name = p_role_name;
    IF v_role_id IS NULL THEN
        RETURN false;
    END IF;
    UPDATE users
    SET full_name = p_full_name,
        role_id = v_role_id,
        is_active = p_is_active,
        updated_by = p_actor_id,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_user_id;
    RETURN FOUND;
END;
$function$;
