CREATE OR REPLACE FUNCTION public.fn_student_can_view_bill(p_bill_id uuid, p_student_id uuid)
RETURNS boolean LANGUAGE sql STABLE AS $function$
    SELECT EXISTS (
        SELECT 1 FROM bills AS bill
        JOIN rooms AS room ON room.id = bill.room_id
        JOIN beds AS bed ON bed.room_id = room.id
        JOIN bed_assignments AS ba ON ba.bed_id = bed.id
        JOIN contracts AS c ON c.id = ba.contract_id
        WHERE bill.id = p_bill_id AND c.student_id = p_student_id
          AND ba.start_date <= bill.period_end
          AND COALESCE(ba.end_date, c.end_date) >= bill.period_start
    );
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_room_bills(
    p_user_id uuid, p_role text, p_room_id uuid
) RETURNS SETOF bills LANGUAGE sql STABLE AS $function$
    SELECT bill.* FROM bills AS bill
    WHERE bill.room_id IS NOT NULL
      AND (p_room_id IS NULL OR bill.room_id = p_room_id)
      AND (p_role <> 'Student' OR public.fn_student_can_view_bill(bill.id, p_user_id))
    ORDER BY bill.period_end DESC, bill.bill_no DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_generate_room_bill(
    p_id uuid, p_bill_no text, p_room_id uuid, p_period_start date,
    p_period_end date, p_issued_date date, p_due_date date,
    p_idempotency_key text, p_user_id uuid
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE
    v_existing bills%ROWTYPE;
    v_room rooms%ROWTYPE;
    v_reading record;
    v_subtotal numeric(14, 2) := 0;
BEGIN
    IF p_period_end < p_period_start OR p_due_date < p_issued_date THEN
        RETURN 'INVALID_PERIOD';
    END IF;
    PERFORM pg_advisory_xact_lock(hashtextextended(p_idempotency_key, 0));
    SELECT * INTO v_existing FROM bills WHERE idempotency_key = p_idempotency_key;
    IF FOUND THEN
        IF v_existing.room_id IS DISTINCT FROM p_room_id
           OR v_existing.period_start <> p_period_start
           OR v_existing.period_end <> p_period_end THEN
            RETURN 'IDEMPOTENCY_KEY_REUSED';
        END IF;
        RETURN v_existing.id::text;
    END IF;
    SELECT * INTO v_room FROM rooms WHERE id = p_room_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'ROOM_NOT_FOUND'; END IF;
    IF EXISTS (SELECT 1 FROM bills WHERE room_id = p_room_id
               AND period_start = p_period_start AND period_end = p_period_end
               AND status <> 'Void') THEN RETURN 'BILL_PERIOD_ALREADY_EXISTS'; END IF;
    IF (SELECT count(*) FROM meter_readings AS mr
        JOIN meters AS m ON m.id = mr.meter_id
        JOIN utilities AS u ON u.id = m.utility_id
        WHERE m.room_id = p_room_id AND u.code IN ('ELECTRICITY', 'WATER')
          AND mr.period_start = p_period_start AND mr.period_end = p_period_end) <> 2
       OR (SELECT count(DISTINCT u.code) FROM meter_readings AS mr
           JOIN meters AS m ON m.id = mr.meter_id
           JOIN utilities AS u ON u.id = m.utility_id
           WHERE m.room_id = p_room_id AND u.code IN ('ELECTRICITY', 'WATER')
             AND mr.period_start = p_period_start AND mr.period_end = p_period_end) <> 2 THEN
        RETURN 'READINGS_INCOMPLETE';
    END IF;
    INSERT INTO bills (id, bill_no, room_id, period_start, period_end,
                       issued_date, due_date, status, subtotal, adjustment_amount,
                       total_amount, paid_amount, balance_amount, idempotency_key, issued_by)
    VALUES (p_id, p_bill_no, p_room_id, p_period_start, p_period_end,
            p_issued_date, p_due_date, 'Issued', 0, 0, 0, 0, 0,
            p_idempotency_key, p_user_id);
    FOR v_reading IN
        SELECT mr.*, m.meter_code, u.code AS utility_code, u.name AS utility_name
        FROM meter_readings AS mr
        JOIN meters AS m ON m.id = mr.meter_id
        JOIN utilities AS u ON u.id = m.utility_id
        WHERE m.room_id = p_room_id AND u.code IN ('ELECTRICITY', 'WATER')
          AND mr.period_start = p_period_start AND mr.period_end = p_period_end
        ORDER BY u.code
    LOOP
        INSERT INTO bill_items (id, bill_id, item_type, reference_type, reference_id,
                                description, quantity, unit_price, amount, calculation_snapshot)
        VALUES (gen_random_uuid(), p_id, initcap(v_reading.utility_code),
                'MeterReading', v_reading.id,
                v_reading.utility_name || ' - ' || v_reading.meter_code,
                v_reading.consumption,
                CASE WHEN v_reading.consumption = 0 THEN 0
                     ELSE round(v_reading.calculated_amount / v_reading.consumption, 2) END,
                v_reading.calculated_amount,
                jsonb_build_object('meter_code', v_reading.meter_code,
                                   'previous_reading', v_reading.previous_reading,
                                   'current_reading', v_reading.current_reading,
                                   'tariff', v_reading.tariff_snapshot)::json);
        v_subtotal := v_subtotal + v_reading.calculated_amount;
    END LOOP;
    UPDATE bills SET subtotal = v_subtotal, total_amount = v_subtotal,
                     balance_amount = v_subtotal, updated_at = CURRENT_TIMESTAMP
    WHERE id = p_id;
    RETURN p_id::text;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_confirm_room_bill_payment(
    p_bill_id uuid, p_method text, p_reference text, p_actor_id uuid
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE v_bill bills%ROWTYPE;
BEGIN
    SELECT * INTO v_bill FROM bills WHERE id = p_bill_id AND room_id IS NOT NULL FOR UPDATE;
    IF NOT FOUND THEN RETURN 'BILL_NOT_FOUND'; END IF;
    IF v_bill.status <> 'Issued' THEN RETURN 'BILL_NOT_PAYABLE'; END IF;
    UPDATE bills SET status = 'Paid', paid_amount = total_amount,
                     balance_amount = 0, payment_method = trim(p_method),
                     payment_reference = nullif(trim(p_reference), ''),
                     paid_at = CURRENT_TIMESTAMP, payment_recorded_by = p_actor_id,
                     updated_at = CURRENT_TIMESTAMP
    WHERE id = p_bill_id;
    RETURN 'OK';
END;
$function$;
