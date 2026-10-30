CREATE OR REPLACE FUNCTION public.fn_list_buildings()
RETURNS SETOF buildings
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM buildings ORDER BY code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_building(p_id uuid)
RETURNS SETOF buildings
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM buildings WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_rooms(p_building_id uuid DEFAULT NULL, p_staff_id uuid DEFAULT NULL)
RETURNS TABLE (
    id uuid, building_id uuid, building_code text, code text, floor integer,
    gender_policy text, managed_by_staff_id uuid, status text,
    is_active boolean, note text, capacity integer, monthly_rate numeric
)
LANGUAGE sql STABLE
AS $function$
    SELECT r.id, r.building_id, b.code::text, r.code::text, r.floor,
           r.gender_policy::text, r.managed_by_staff_id, r.status::text,
           r.is_active, r.note::text, r.capacity, r.monthly_rate
    FROM rooms AS r
    JOIN buildings AS b ON b.id = r.building_id
    WHERE (p_building_id IS NULL OR r.building_id = p_building_id)
      AND (p_staff_id IS NULL OR r.managed_by_staff_id = p_staff_id)
    ORDER BY r.floor, r.code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_room(p_id uuid)
RETURNS TABLE (
    id uuid, building_id uuid, building_code text, code text, floor integer,
    gender_policy text, managed_by_staff_id uuid, status text,
    is_active boolean, note text, capacity integer, monthly_rate numeric
)
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM public.fn_list_rooms(NULL, NULL) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_beds(p_room_id uuid DEFAULT NULL, p_staff_id uuid DEFAULT NULL)
RETURNS TABLE (id uuid, room_id uuid, code text, is_active boolean, note text, status text)
LANGUAGE sql STABLE
AS $function$
    SELECT bed.id, bed.room_id, bed.code::text, bed.is_active, bed.note::text,
           CASE WHEN NOT bed.is_active THEN 'Maintenance'
                WHEN EXISTS (
                    SELECT 1 FROM bed_assignments AS a
                    WHERE a.bed_id = bed.id AND a.status = 'Active'
                ) THEN 'Occupied'
                ELSE 'Available' END::text
    FROM beds AS bed
    JOIN rooms AS room ON room.id = bed.room_id
    WHERE (p_room_id IS NULL OR bed.room_id = p_room_id)
      AND (p_staff_id IS NULL OR room.managed_by_staff_id = p_staff_id)
    ORDER BY bed.code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_bed(p_id uuid)
RETURNS TABLE (id uuid, room_id uuid, code text, is_active boolean, note text, status text)
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM public.fn_list_beds(NULL, NULL) WHERE id = p_id;
$function$;
