CREATE OR REPLACE FUNCTION public.fn_get_bill(p_id uuid)
RETURNS SETOF bills LANGUAGE sql STABLE AS $function$
    SELECT * FROM bills WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_bills(p_user_id uuid, p_role text,
                                                p_contract_id uuid)
RETURNS SETOF bills LANGUAGE sql STABLE AS $function$
    SELECT * FROM bills
    WHERE (p_role <> 'Student' OR student_id = p_user_id)
      AND (p_contract_id IS NULL OR contract_id = p_contract_id)
    ORDER BY issued_date DESC, bill_no DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_bill_items(p_bill_id uuid)
RETURNS SETOF bill_items LANGUAGE sql STABLE AS $function$
    SELECT * FROM bill_items WHERE bill_id = p_bill_id ORDER BY created_at, item_type;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_generate_bill(
    p_id uuid, p_bill_no text, p_contract_id uuid, p_period_start date,
    p_period_end date, p_issued_date date, p_due_date date,
    p_idempotency_key text, p_user_id uuid
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE
    v_existing bills%ROWTYPE;
    v_contract contracts%ROWTYPE;
    v_room_ids uuid[];
    v_reading record;
    v_subtotal numeric(14, 2);
    v_unit_price numeric(14, 2);
BEGIN
    PERFORM pg_advisory_xact_lock(hashtextextended(p_idempotency_key, 0));
    SELECT * INTO v_existing FROM bills WHERE idempotency_key = p_idempotency_key;
    IF FOUND THEN
        IF v_existing.contract_id <> p_contract_id
           OR v_existing.period_start <> p_period_start
           OR v_existing.period_end <> p_period_end THEN
            RETURN 'IDEMPOTENCY_KEY_REUSED';
        END IF;
        RETURN v_existing.id::text;
    END IF;

    SELECT * INTO v_contract FROM contracts WHERE id = p_contract_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'CONTRACT_NOT_FOUND'; END IF;
    IF p_period_end < v_contract.start_date OR p_period_start > v_contract.end_date THEN
        RETURN 'BILL_PERIOD_OUTSIDE_CONTRACT';
    END IF;
    IF EXISTS (SELECT 1 FROM bills WHERE contract_id = p_contract_id
               AND period_start = p_period_start AND period_end = p_period_end
               AND status <> 'Void') THEN
        RETURN 'BILL_PERIOD_ALREADY_EXISTS';
    END IF;
    SELECT array_agg(DISTINCT r.id) INTO v_room_ids
    FROM rooms r JOIN beds b ON b.room_id = r.id
    JOIN bed_assignments ba ON ba.bed_id = b.id
    WHERE ba.contract_id = p_contract_id AND ba.start_date <= p_period_end
      AND (ba.end_date IS NULL OR ba.end_date >= p_period_start);
    IF v_room_ids IS NULL THEN RETURN 'BILL_ROOM_NOT_FOUND'; END IF;

    INSERT INTO bills (id, bill_no, contract_id, student_id, period_start,
                       period_end, issued_date, due_date, status, subtotal,
                       adjustment_amount, total_amount, paid_amount,
                       balance_amount, idempotency_key, issued_by)
    VALUES (p_id, p_bill_no, p_contract_id, v_contract.student_id, p_period_start,
            p_period_end, p_issued_date, p_due_date, 'Issued', 0, 0, 0, 0, 0,
            p_idempotency_key, p_user_id);

    INSERT INTO bill_items (id, bill_id, item_type, reference_type, reference_id,
                            description, quantity, unit_price, amount, calculation_snapshot)
    VALUES (gen_random_uuid(), p_id, 'Housing', 'Contract', p_contract_id,
            format('Phí phòng kỳ %s - %s', to_char(p_period_start, 'DD/MM/YYYY'),
                   to_char(p_period_end, 'DD/MM/YYYY')),
            1, v_contract.base_rate, v_contract.base_rate,
            jsonb_build_object('contract_no', v_contract.contract_no,
                               'base_rate', v_contract.base_rate::text)::json);
    v_subtotal := v_contract.base_rate;

    FOR v_reading IN
        SELECT mr.id, mr.consumption, mr.calculated_amount, mr.previous_reading,
               mr.current_reading, mr.tariff_snapshot, m.meter_code,
               u.code AS utility_code, u.name AS utility_name
        FROM meter_readings mr JOIN meters m ON m.id = mr.meter_id
        JOIN utilities u ON u.id = m.utility_id
        WHERE m.room_id = ANY(v_room_ids) AND mr.period_start = p_period_start
          AND mr.period_end = p_period_end
        ORDER BY u.code, m.meter_code
    LOOP
        v_unit_price := CASE WHEN v_reading.consumption = 0 THEN 0
                        ELSE round(v_reading.calculated_amount / v_reading.consumption, 2)
                        END;
        INSERT INTO bill_items (id, bill_id, item_type, reference_type, reference_id,
                                description, quantity, unit_price, amount,
                                calculation_snapshot)
        VALUES (gen_random_uuid(), p_id, initcap(v_reading.utility_code),
                'MeterReading', v_reading.id,
                v_reading.utility_name || ' - công tơ ' || v_reading.meter_code,
                v_reading.consumption, v_unit_price, v_reading.calculated_amount,
                jsonb_build_object('meter_code', v_reading.meter_code,
                    'previous_reading', v_reading.previous_reading::text,
                    'current_reading', v_reading.current_reading::text,
                    'tariff', v_reading.tariff_snapshot)::json);
        v_subtotal := v_subtotal + v_reading.calculated_amount;
    END LOOP;
    UPDATE bills SET subtotal = v_subtotal, total_amount = v_subtotal,
                     balance_amount = v_subtotal, updated_at = CURRENT_TIMESTAMP
    WHERE id = p_id;
    RETURN p_id::text;
END;
$function$;
