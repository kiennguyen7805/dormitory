-- Frozen for migration 0017; keep independent of later schema changes.
CREATE OR REPLACE FUNCTION public.fn_save_housing(
    p_entity text, p_id uuid, p_data jsonb, p_create boolean
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
BEGIN
    CASE p_entity
        WHEN 'building' THEN
            IF p_create THEN
                INSERT INTO buildings (id, code, name, address, floors, is_active)
                VALUES (
                    p_id, upper(trim(p_data->>'code')), p_data->>'name',
                    p_data->>'address', (p_data->>'floors')::integer,
                    (p_data->>'is_active')::boolean
                );
                RETURN true;
            END IF;
            UPDATE buildings SET
                code = upper(trim(p_data->>'code')),
                name = p_data->>'name', address = p_data->>'address',
                floors = (p_data->>'floors')::integer,
                is_active = (p_data->>'is_active')::boolean,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            RETURN FOUND;
        WHEN 'room_type' THEN
            IF p_create THEN
                INSERT INTO room_types (
                    id, name, default_monthly_rate, default_capacity,
                    description, is_active
                ) VALUES (
                    p_id, trim(p_data->>'name'),
                    (p_data->>'default_monthly_rate')::numeric,
                    (p_data->>'default_capacity')::integer,
                    p_data->>'description', (p_data->>'is_active')::boolean
                );
                RETURN true;
            END IF;
            UPDATE room_types SET
                name = trim(p_data->>'name'),
                default_monthly_rate = (p_data->>'default_monthly_rate')::numeric,
                default_capacity = (p_data->>'default_capacity')::integer,
                description = p_data->>'description',
                is_active = (p_data->>'is_active')::boolean,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            RETURN FOUND;
        WHEN 'room' THEN
            IF p_create THEN
                INSERT INTO rooms (
                    id, building_id, room_type_id, code, floor, gender_policy,
                    managed_by_staff_id, status, is_active, note
                ) VALUES (
                    p_id, (p_data->>'building_id')::uuid,
                    (p_data->>'room_type_id')::uuid, upper(trim(p_data->>'code')),
                    (p_data->>'floor')::integer, p_data->>'gender_policy',
                    (p_data->>'managed_by_staff_id')::uuid, p_data->>'status',
                    (p_data->>'is_active')::boolean, p_data->>'note'
                );
                RETURN true;
            END IF;
            UPDATE rooms SET
                building_id = (p_data->>'building_id')::uuid,
                room_type_id = (p_data->>'room_type_id')::uuid,
                code = upper(trim(p_data->>'code')),
                floor = (p_data->>'floor')::integer,
                gender_policy = p_data->>'gender_policy',
                managed_by_staff_id = (p_data->>'managed_by_staff_id')::uuid,
                status = p_data->>'status',
                is_active = (p_data->>'is_active')::boolean,
                note = p_data->>'note', updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            RETURN FOUND;
        WHEN 'bed' THEN
            IF p_create THEN
                INSERT INTO beds (id, room_id, code, is_active, note)
                VALUES (
                    p_id, (p_data->>'room_id')::uuid,
                    upper(trim(p_data->>'code')),
                    (p_data->>'is_active')::boolean, p_data->>'note'
                );
                RETURN true;
            END IF;
            UPDATE beds SET
                room_id = (p_data->>'room_id')::uuid,
                code = upper(trim(p_data->>'code')),
                is_active = (p_data->>'is_active')::boolean,
                note = p_data->>'note', updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            RETURN FOUND;
        ELSE
            RAISE EXCEPTION 'Unknown housing entity';
    END CASE;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_deactivate_housing(p_entity text, p_id uuid)
RETURNS integer
LANGUAGE plpgsql
AS $function$
BEGIN
    CASE p_entity
        WHEN 'building' THEN
            PERFORM 1 FROM buildings WHERE id = p_id FOR UPDATE;
            IF NOT FOUND THEN RETURN 0; END IF;
            IF EXISTS (
                SELECT 1 FROM bed_assignments AS a
                JOIN beds AS bed ON bed.id = a.bed_id
                JOIN rooms AS room ON room.id = bed.room_id
                WHERE room.building_id = p_id AND a.status = 'Active'
            ) THEN RETURN -1; END IF;
            UPDATE buildings SET is_active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
        WHEN 'room_type' THEN
            UPDATE room_types SET is_active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            IF NOT FOUND THEN RETURN 0; END IF;
        WHEN 'room' THEN
            PERFORM 1 FROM rooms WHERE id = p_id FOR UPDATE;
            IF NOT FOUND THEN RETURN 0; END IF;
            IF EXISTS (
                SELECT 1 FROM bed_assignments AS a
                JOIN beds AS bed ON bed.id = a.bed_id
                WHERE bed.room_id = p_id AND a.status = 'Active'
            ) THEN RETURN -1; END IF;
            UPDATE rooms SET is_active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
        WHEN 'bed' THEN
            PERFORM 1 FROM beds WHERE id = p_id FOR UPDATE;
            IF NOT FOUND THEN RETURN 0; END IF;
            IF EXISTS (
                SELECT 1 FROM bed_assignments
                WHERE bed_id = p_id AND status = 'Active'
            ) THEN RETURN -1; END IF;
            UPDATE beds SET is_active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
        ELSE
            RAISE EXCEPTION 'Unknown housing entity';
    END CASE;
    RETURN 1;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_bulk_update_room_gender(
    p_room_ids uuid[], p_building_id uuid, p_floor integer,
    p_gender_policy text, p_actor_id uuid, p_is_admin boolean
)
RETURNS integer
LANGUAGE plpgsql
AS $function$
DECLARE
    v_room_ids uuid[] := ARRAY[]::uuid[];
    v_room_id uuid;
BEGIN
    IF cardinality(p_room_ids) = 0 AND p_building_id IS NULL THEN
        RETURN -1;
    END IF;
    FOR v_room_id IN
        SELECT id FROM rooms
        WHERE (cardinality(p_room_ids) > 0 AND id = ANY(p_room_ids))
           OR (cardinality(p_room_ids) = 0 AND building_id = p_building_id
               AND (p_floor IS NULL OR floor = p_floor))
        FOR UPDATE
    LOOP
        v_room_ids := array_append(v_room_ids, v_room_id);
    END LOOP;
    IF cardinality(v_room_ids) = 0 THEN RETURN -2; END IF;
    IF NOT p_is_admin AND EXISTS (
        SELECT 1 FROM rooms
        WHERE id = ANY(v_room_ids) AND managed_by_staff_id IS DISTINCT FROM p_actor_id
    ) THEN RETURN -3; END IF;
    IF EXISTS (
        SELECT 1 FROM bed_assignments AS a
        JOIN beds AS bed ON bed.id = a.bed_id
        WHERE bed.room_id = ANY(v_room_ids) AND a.status = 'Active'
    ) THEN RETURN -4; END IF;
    UPDATE rooms SET gender_policy = p_gender_policy,
                     updated_by = p_actor_id, updated_at = CURRENT_TIMESTAMP
    WHERE id = ANY(v_room_ids);
    RETURN cardinality(v_room_ids);
END;
$function$;
