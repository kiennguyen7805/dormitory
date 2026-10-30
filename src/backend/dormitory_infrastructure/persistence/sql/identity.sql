-- Public result contract for GET /api/v1/users.
-- The API may continue calling this function while the SELECT body is optimized.
CREATE OR REPLACE FUNCTION public.fn_list_users(p_role text DEFAULT NULL)
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
    SELECT
        u.id,
        u.email::text,
        u.full_name::text,
        r.name::text,
        u.is_active
    FROM users AS u
    JOIN roles AS r ON r.id = u.role_id
    WHERE p_role IS NULL OR r.name = p_role
    ORDER BY u.full_name;
$function$;
