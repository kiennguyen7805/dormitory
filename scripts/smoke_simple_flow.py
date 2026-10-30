"""Run against a disposable seeded database: DATABASE_URL=... python smoke_simple_flow.py."""

import os
import sys
from datetime import date
from pathlib import Path
from uuid import uuid4

import psycopg


BACKEND = Path(__file__).resolve().parents[1] / "src" / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


url = os.environ["DATABASE_URL"].replace("postgresql+psycopg://", "postgresql://")
with psycopg.connect(url) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM roles WHERE name = 'Student'")
        student_role = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM users WHERE email = 'admin@dormitory.local'")
        admin = cursor.fetchone()
        if admin is None:
            cursor.execute("SELECT id FROM users LIMIT 1")
            admin = cursor.fetchone()
        admin_id = admin[0]
        students = [uuid4(), uuid4()]
        for index, student_id in enumerate(students):
            cursor.execute(
                "INSERT INTO users (id, email, full_name, password_hash, is_active, role_id) "
                "VALUES (%s, %s, %s, 'test-hash', true, %s)",
                (student_id, f"room-smoke-{index}-{student_id}@test.local", f"Student {index}", student_role),
            )
        building_id, room_id = uuid4(), uuid4()
        cursor.execute(
            "INSERT INTO buildings (id, code, name, address, floors, is_active) "
            "VALUES (%s, %s, 'Smoke building', '', 2, true)",
            (building_id, f"T{str(building_id)[:6]}"),
        )
        cursor.execute("SELECT fn_create_simple_room(%s, %s, '101', 1, 2, 100000)",
                       (room_id, building_id))
        assert cursor.fetchone()[0] == "OK"
        cursor.execute("SELECT count(*) FROM beds WHERE room_id = %s", (room_id,))
        assert cursor.fetchone()[0] == 2
        cursor.execute("SELECT count(*) FROM meters WHERE room_id = %s", (room_id,))
        assert cursor.fetchone()[0] == 2
        for student_id in students:
            application_id, contract_id, assignment_id = uuid4(), uuid4(), uuid4()
            cursor.execute("SELECT fn_create_application(%s, %s, '2026-10', %s)",
                           (application_id, student_id, room_id))
            assert cursor.fetchone()[0] == "OK"
            cursor.execute("SELECT fn_review_application(%s, %s, 'Approved', NULL)",
                           (application_id, admin_id))
            assert cursor.fetchone()[0] == "OK"
            cursor.execute(
                "SELECT fn_assign_room(%s, %s, %s, %s, %s, %s)",
                (application_id, contract_id, assignment_id, f"HD-{contract_id}",
                 date(2026, 10, 1), date(2027, 6, 30)),
            )
            assert cursor.fetchone()[0] == "OK"
        cursor.execute("SELECT id, utility_id FROM meters WHERE room_id = %s ORDER BY meter_code", (room_id,))
        for meter_id, utility_id in cursor.fetchall():
            tariff_id = uuid4()
            cursor.execute(
                "INSERT INTO utility_tariffs "
                "(id, utility_id, name, effective_from, calculation_type, is_active) "
                "VALUES (%s, %s, 'Smoke tariff', %s, 'Flat', true)",
                (tariff_id, utility_id, date(2026, 10, 1)),
            )
            cursor.execute(
                "INSERT INTO meter_readings "
                "(id, meter_id, period_start, period_end, previous_reading, current_reading, "
                "consumption, tariff_id, tariff_snapshot, calculated_amount) "
                "VALUES (%s, %s, %s, %s, 0, 10, 10, %s, '{}', 125)",
                (uuid4(), meter_id, date(2026, 10, 1), date(2026, 10, 31), tariff_id),
            )
        bill_id = uuid4()
        args = (bill_id, f"HD-{bill_id}", room_id, date(2026, 10, 1),
                date(2026, 10, 31), date(2026, 11, 1), date(2026, 11, 15),
                str(bill_id), admin_id)
        cursor.execute("SELECT fn_generate_room_bill(%s,%s,%s,%s,%s,%s,%s,%s,%s)", args)
        assert cursor.fetchone()[0] == str(bill_id)
        cursor.execute("SELECT total_amount, room_id, contract_id, student_id FROM bills WHERE id = %s", (bill_id,))
        total, actual_room, contract_id, student_id = cursor.fetchone()
        assert total == 250 and actual_room == room_id and contract_id is None and student_id is None
        cursor.execute("SELECT count(*) FROM bill_items WHERE bill_id = %s", (bill_id,))
        assert cursor.fetchone()[0] == 2
        for student_id in students:
            cursor.execute("SELECT fn_student_can_view_bill(%s, %s)", (bill_id, student_id))
            assert cursor.fetchone()[0] is True
            cursor.execute("SELECT count(*) FROM fn_list_room_bills(%s, 'Student', NULL)", (student_id,))
            assert cursor.fetchone()[0] == 1
        cursor.execute("SELECT fn_generate_room_bill(%s,%s,%s,%s,%s,%s,%s,%s,%s)", args)
        assert cursor.fetchone()[0] == str(bill_id)
        cursor.execute("SELECT fn_confirm_room_bill_payment(%s, 'Cash', 'SMOKE', %s)",
                       (bill_id, admin_id))
        assert cursor.fetchone()[0] == "OK"
        cursor.execute("SELECT status, paid_amount, balance_amount FROM bills WHERE id = %s", (bill_id,))
        assert cursor.fetchone() == ("Paid", 250, 0)
        cursor.execute("SELECT fn_confirm_room_bill_payment(%s, 'Cash', 'SMOKE', %s)",
                       (bill_id, admin_id))
        assert cursor.fetchone()[0] == "BILL_NOT_PAYABLE"
        print("PASS: two students, one room bill, two utility items, one payment")

from sqlalchemy import create_engine
from dormitory_infrastructure.persistence.repositories.billing import StoredBillingRepository

engine = create_engine(os.environ["DATABASE_URL"])
with engine.connect() as connection:
    repository = StoredBillingRepository(connection)
    for student_id in students:
        bills = repository.list_bills(student_id, "Student", room_id)
        assert len(bills) == 1
        assert bills[0].status == "Paid" and bills[0].total_amount == 250
        assert len(bills[0].items) == 2
        assert repository.get_bill(bill_id, student_id, "Student").id == bill_id
print("PASS: repository validates the shared bill for both students")
