CREATE OR REPLACE FUNCTION public.fn_list_utilities()
RETURNS SETOF utilities LANGUAGE sql STABLE AS $function$
    SELECT * FROM utilities WHERE is_active = true ORDER BY code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_meters(p_room_id uuid)
RETURNS TABLE (
    id uuid, utility_id uuid, utility_code varchar, utility_name varchar,
    room_id uuid, room_label text, meter_code varchar, serial_number varchar,
    initial_reading numeric, is_active boolean
) LANGUAGE sql STABLE AS $function$
    SELECT m.id, m.utility_id, u.code, u.name, m.room_id,
           b.code || '-' || r.code, m.meter_code, m.serial_number,
           m.initial_reading, m.is_active
    FROM meters m JOIN utilities u ON u.id = m.utility_id
    JOIN rooms r ON r.id = m.room_id JOIN buildings b ON b.id = r.building_id
    WHERE p_room_id IS NULL OR m.room_id = p_room_id
    ORDER BY b.code, r.code, u.code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_meter(p_id uuid)
RETURNS TABLE (
    id uuid, utility_id uuid, utility_code varchar, utility_name varchar,
    room_id uuid, room_label text, meter_code varchar, serial_number varchar,
    initial_reading numeric, is_active boolean
) LANGUAGE sql STABLE AS $function$
    SELECT * FROM public.fn_list_meters(NULL::uuid) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_create_meter(
    p_id uuid, p_utility_id uuid, p_room_id uuid, p_meter_code text,
    p_serial_number text, p_installed_at date, p_initial_reading numeric, p_note text
) RETURNS text LANGUAGE plpgsql AS $function$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM utilities WHERE id = p_utility_id AND is_active) THEN
        RETURN 'UTILITY_NOT_FOUND';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM rooms WHERE id = p_room_id AND is_active) THEN
        RETURN 'ROOM_NOT_FOUND';
    END IF;
    INSERT INTO meters (id, utility_id, room_id, meter_code, serial_number,
                        installed_at, initial_reading, note, is_active)
    VALUES (p_id, p_utility_id, p_room_id, upper(trim(p_meter_code)),
            nullif(trim(p_serial_number), ''), p_installed_at, p_initial_reading, p_note, true);
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_tariffs(p_utility_id uuid)
RETURNS TABLE (
    id uuid, utility_id uuid, utility_code varchar, utility_name varchar,
    name varchar, effective_from date, effective_to date,
    calculation_type varchar, is_active boolean
) LANGUAGE sql STABLE AS $function$
    SELECT t.id, t.utility_id, u.code, u.name, t.name, t.effective_from,
           t.effective_to, t.calculation_type, t.is_active
    FROM utility_tariffs t JOIN utilities u ON u.id = t.utility_id
    WHERE p_utility_id IS NULL OR t.utility_id = p_utility_id
    ORDER BY u.code, t.effective_from DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_tariff(p_id uuid)
RETURNS TABLE (
    id uuid, utility_id uuid, utility_code varchar, utility_name varchar,
    name varchar, effective_from date, effective_to date,
    calculation_type varchar, is_active boolean
) LANGUAGE sql STABLE AS $function$
    SELECT * FROM public.fn_list_tariffs(NULL::uuid) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_tariff_tiers(p_tariff_id uuid)
RETURNS SETOF tariff_tiers LANGUAGE sql STABLE AS $function$
    SELECT * FROM tariff_tiers WHERE tariff_id = p_tariff_id ORDER BY tier_order;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_create_tariff(
    p_id uuid, p_utility_id uuid, p_name text, p_effective_from date,
    p_effective_to date, p_calculation_type text, p_created_by uuid, p_tiers jsonb
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE v_tier jsonb;
BEGIN
    PERFORM 1 FROM utilities WHERE id = p_utility_id AND is_active FOR UPDATE;
    IF NOT FOUND THEN RETURN 'UTILITY_NOT_FOUND'; END IF;
    IF EXISTS (
        SELECT 1 FROM utility_tariffs WHERE utility_id = p_utility_id AND is_active
          AND (effective_to IS NULL OR effective_to >= p_effective_from)
          AND (p_effective_to IS NULL OR effective_from <= p_effective_to)
    ) THEN RETURN 'TARIFF_PERIOD_OVERLAP'; END IF;
    INSERT INTO utility_tariffs (id, utility_id, name, effective_from, effective_to,
                                 calculation_type, is_active, created_by)
    VALUES (p_id, p_utility_id, trim(p_name), p_effective_from, p_effective_to,
            p_calculation_type, true, p_created_by);
    FOR v_tier IN SELECT value FROM jsonb_array_elements(p_tiers) LOOP
        INSERT INTO tariff_tiers (id, tariff_id, tier_order, from_quantity,
                                  to_quantity, unit_price)
        VALUES ((v_tier->>'id')::uuid, p_id, (v_tier->>'tier_order')::integer,
                (v_tier->>'from_quantity')::numeric,
                (v_tier->>'to_quantity')::numeric,
                (v_tier->>'unit_price')::numeric);
    END LOOP;
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_find_tariff(p_utility_id uuid, p_period_end date)
RETURNS SETOF utility_tariffs LANGUAGE sql STABLE AS $function$
    SELECT * FROM utility_tariffs
    WHERE utility_id = p_utility_id AND is_active
      AND effective_from <= p_period_end
      AND (effective_to IS NULL OR effective_to >= p_period_end)
    ORDER BY effective_from DESC LIMIT 1;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_readings(p_meter_id uuid, p_period_start date)
RETURNS TABLE (
    id uuid, meter_id uuid, meter_code varchar, utility_code varchar,
    period_start date, period_end date, previous_reading numeric,
    current_reading numeric, consumption numeric, calculated_amount numeric,
    tariff_id uuid, tariff_snapshot json, recorded_at timestamptz
) LANGUAGE sql STABLE AS $function$
    SELECT mr.id, mr.meter_id, m.meter_code, u.code, mr.period_start,
           mr.period_end, mr.previous_reading, mr.current_reading,
           mr.consumption, mr.calculated_amount, mr.tariff_id,
           mr.tariff_snapshot, mr.recorded_at
    FROM meter_readings mr JOIN meters m ON m.id = mr.meter_id
    JOIN utilities u ON u.id = m.utility_id
    WHERE (p_meter_id IS NULL OR mr.meter_id = p_meter_id)
      AND (p_period_start IS NULL OR mr.period_start = p_period_start)
    ORDER BY mr.recorded_at DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_reading(p_id uuid)
RETURNS TABLE (
    id uuid, meter_id uuid, meter_code varchar, utility_code varchar,
    period_start date, period_end date, previous_reading numeric,
    current_reading numeric, consumption numeric, calculated_amount numeric,
    tariff_id uuid, tariff_snapshot json, recorded_at timestamptz
) LANGUAGE sql STABLE AS $function$
    SELECT * FROM public.fn_list_readings(NULL::uuid, NULL::date) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_reading_context(p_meter_id uuid, p_period_start date,
                                                      p_period_end date)
RETURNS TABLE (
    meter_id uuid, utility_id uuid, initial_reading numeric, is_active boolean,
    duplicate_id uuid, previous_reading numeric
) LANGUAGE plpgsql AS $function$
BEGIN
    PERFORM 1 FROM meters WHERE id = p_meter_id FOR UPDATE;
    RETURN QUERY SELECT m.id, m.utility_id, m.initial_reading, m.is_active,
        (SELECT mr.id FROM meter_readings mr WHERE mr.meter_id = m.id
         AND mr.period_start = p_period_start AND mr.period_end = p_period_end LIMIT 1),
        (SELECT mr.current_reading FROM meter_readings mr WHERE mr.meter_id = m.id
         AND mr.period_end < p_period_start ORDER BY mr.period_end DESC LIMIT 1)
    FROM meters m WHERE m.id = p_meter_id;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_create_reading(
    p_id uuid, p_meter_id uuid, p_period_start date, p_period_end date,
    p_previous numeric, p_current numeric, p_consumption numeric,
    p_tariff_id uuid, p_snapshot json, p_amount numeric, p_recorded_by uuid
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE v_initial numeric; v_previous numeric; v_utility_id uuid;
BEGIN
    SELECT m.initial_reading, m.utility_id INTO v_initial, v_utility_id
    FROM meters m WHERE m.id = p_meter_id AND m.is_active FOR UPDATE;
    IF NOT FOUND THEN RETURN 'METER_NOT_FOUND'; END IF;
    IF EXISTS (SELECT 1 FROM meter_readings WHERE meter_id = p_meter_id
               AND period_start = p_period_start AND period_end = p_period_end) THEN
        RETURN 'METER_READING_ALREADY_EXISTS';
    END IF;
    SELECT current_reading INTO v_previous FROM meter_readings
    WHERE meter_id = p_meter_id AND period_end < p_period_start
    ORDER BY period_end DESC LIMIT 1;
    IF p_previous <> coalesce(v_previous, v_initial) THEN
        RETURN 'PREVIOUS_READING_MISMATCH';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM utility_tariffs WHERE id = p_tariff_id
                   AND utility_id = v_utility_id AND is_active
                   AND effective_from <= p_period_end
                   AND (effective_to IS NULL OR effective_to >= p_period_end)) THEN
        RETURN 'TARIFF_NOT_FOUND';
    END IF;
    INSERT INTO meter_readings (id, meter_id, period_start, period_end,
        previous_reading, current_reading, consumption, tariff_id,
        tariff_snapshot, calculated_amount, recorded_by)
    VALUES (p_id, p_meter_id, p_period_start, p_period_end,
            p_previous, p_current, p_consumption, p_tariff_id,
            p_snapshot, p_amount, p_recorded_by);
    RETURN 'OK';
END;
$function$;
