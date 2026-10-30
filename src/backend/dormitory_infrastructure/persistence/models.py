from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Uuid, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Uuid, ForeignKey("permissions.id"), primary_key=True),
)


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(300))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    users: Mapped[list["UserModel"]] = relationship(back_populates="role")
    permissions: Mapped[list["PermissionModel"]] = relationship(
        secondary=role_permissions, back_populates="roles"
    )


class PermissionModel(Base):
    __tablename__ = "permissions"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    module: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(300))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    roles: Mapped[list[RoleModel]] = relationship(
        secondary=role_permissions, back_populates="permissions"
    )


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)
    last_password_changed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    refresh_token_hash: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    refresh_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    refresh_token_revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    role: Mapped[RoleModel] = relationship(back_populates="users")
    student_profile: Mapped["StudentProfileModel | None"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class StudentProfileModel(Base):
    __tablename__ = "student_profiles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    student_code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    faculty: Mapped[str] = mapped_column(String(150), default="", nullable=False)
    cohort: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    gender: Mapped[str | None] = mapped_column(String(20))
    phone: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    address: Mapped[str] = mapped_column(String(300), default="", nullable=False)
    identity_number: Mapped[str | None] = mapped_column(String(30))
    emergency_contact_name: Mapped[str] = mapped_column(String(120), default="", nullable=False)
    emergency_contact_phone: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    user: Mapped[UserModel] = relationship(back_populates="student_profile")


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str] = mapped_column(String(250), default="", nullable=False)
    floors: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    rooms: Mapped[list["RoomModel"]] = relationship(
        back_populates="building", cascade="all, delete-orphan"
    )


class RoomTypeModel(Base):
    __tablename__ = "room_types"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    default_monthly_rate: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    default_capacity: Mapped[int | None] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    rooms: Mapped[list["RoomModel"]] = relationship(back_populates="room_type")


class RoomModel(Base):
    __tablename__ = "rooms"
    __table_args__ = (UniqueConstraint("building_id", "code", name="uq_rooms_building_code"),)

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    building_id: Mapped[UUID] = mapped_column(ForeignKey("buildings.id"), nullable=False)
    room_type_id: Mapped[UUID] = mapped_column(ForeignKey("room_types.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    gender_policy: Mapped[str] = mapped_column(String(20), default="Unassigned", nullable=False)
    managed_by_staff_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(20), default="Available", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    note: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    building: Mapped[BuildingModel] = relationship(back_populates="rooms")
    room_type: Mapped[RoomTypeModel] = relationship(back_populates="rooms")
    beds: Mapped[list["BedModel"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )


class BedModel(Base):
    __tablename__ = "beds"
    __table_args__ = (UniqueConstraint("room_id", "code", name="uq_beds_room_code"),)

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    room_id: Mapped[UUID] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    note: Mapped[str | None] = mapped_column(String(300))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    room: Mapped[RoomModel] = relationship(back_populates="beds")
    assignments: Mapped[list["BedAssignmentModel"]] = relationship(back_populates="bed")


class HousingApplicationModel(Base):
    __tablename__ = "housing_applications"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    term_code: Mapped[str] = mapped_column(String(30), nullable=False)
    preferred_room_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("room_types.id"), nullable=False
    )
    expected_start_date: Mapped[date | None] = mapped_column(Date)
    expected_end_date: Mapped[date | None] = mapped_column(Date)
    note: Mapped[str | None] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Submitted", index=True
    )
    rejection_reason: Mapped[str | None] = mapped_column(String(500))
    reviewed_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    student: Mapped[UserModel] = relationship(foreign_keys=[student_id])
    preferred_room_type: Mapped[RoomTypeModel] = relationship()
    contract: Mapped["ContractModel | None"] = relationship(
        back_populates="application", uselist=False
    )


class ContractModel(Base):
    __tablename__ = "contracts"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    contract_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    application_id: Mapped[UUID] = mapped_column(
        ForeignKey("housing_applications.id"), unique=True, nullable=False
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Active", index=True
    )
    base_rate: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    issued_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    terminated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    termination_reason: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    student: Mapped[UserModel] = relationship(foreign_keys=[student_id])
    application: Mapped[HousingApplicationModel] = relationship(back_populates="contract")
    assignments: Mapped[list["BedAssignmentModel"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )


class BedAssignmentModel(Base):
    __tablename__ = "bed_assignments"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    contract_id: Mapped[UUID] = mapped_column(
        ForeignKey("contracts.id"), nullable=False, index=True
    )
    bed_id: Mapped[UUID] = mapped_column(ForeignKey("beds.id"), nullable=False, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Active", index=True
    )
    assigned_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    ended_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    end_reason: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    contract: Mapped[ContractModel] = relationship(back_populates="assignments")
    bed: Mapped[BedModel] = relationship(back_populates="assignments")


class RoomTransferRequestModel(Base):
    __tablename__ = "room_transfer_requests"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    contract_id: Mapped[UUID] = mapped_column(ForeignKey("contracts.id"), nullable=False, index=True)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    current_bed_id: Mapped[UUID] = mapped_column(ForeignKey("beds.id"), nullable=False)
    preferred_room_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("room_types.id"))
    preferred_building_id: Mapped[UUID | None] = mapped_column(ForeignKey("buildings.id"))
    requested_bed_id: Mapped[UUID | None] = mapped_column(ForeignKey("beds.id"))
    reason: Mapped[str] = mapped_column(String(1000), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Submitted", nullable=False)
    reviewed_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[str | None] = mapped_column(String(500))
    assigned_bed_id: Mapped[UUID | None] = mapped_column(ForeignKey("beds.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ContractEventModel(Base):
    __tablename__ = "contract_events"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    contract_id: Mapped[UUID] = mapped_column(ForeignKey("contracts.id"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(40), nullable=False)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    old_status: Mapped[str | None] = mapped_column(String(20))
    new_status: Mapped[str] = mapped_column(String(20), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(500))
    event_data: Mapped[dict | None] = mapped_column(JSON)
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UtilityModel(Base):
    __tablename__ = "utilities"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    rounding_scale: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MeterModel(Base):
    __tablename__ = "meters"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    utility_id: Mapped[UUID] = mapped_column(ForeignKey("utilities.id"), nullable=False)
    room_id: Mapped[UUID] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    meter_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    serial_number: Mapped[str | None] = mapped_column(String(100))
    installed_at: Mapped[date | None] = mapped_column(Date)
    initial_reading: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    retired_at: Mapped[date | None] = mapped_column(Date)
    note: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class UtilityTariffModel(Base):
    __tablename__ = "utility_tariffs"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    utility_id: Mapped[UUID] = mapped_column(ForeignKey("utilities.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date)
    calculation_type: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TariffTierModel(Base):
    __tablename__ = "tariff_tiers"
    __table_args__ = (UniqueConstraint("tariff_id", "tier_order", name="uq_tariff_tiers_order"),)
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    tariff_id: Mapped[UUID] = mapped_column(ForeignKey("utility_tariffs.id"), nullable=False)
    tier_order: Mapped[int] = mapped_column(Integer, nullable=False)
    from_quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    to_quantity: Mapped[Decimal | None] = mapped_column(Numeric(14, 3))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)


class StoredFileModel(Base):
    __tablename__ = "stored_files"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    storage_provider: Mapped[str] = mapped_column(String(30), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(150), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    checksum_sha256: Mapped[str | None] = mapped_column(String(64))
    uploaded_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class UtilityImportBatchModel(Base):
    __tablename__ = "utility_import_batches"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    file_id: Mapped[UUID | None] = mapped_column(ForeignKey("stored_files.id"))
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    total_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    valid_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    invalid_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    preview_rows: Mapped[list | dict | None] = mapped_column(JSON)
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class MeterReadingModel(Base):
    __tablename__ = "meter_readings"
    __table_args__ = (UniqueConstraint("meter_id", "period_start", "period_end", name="uq_meter_readings_period"),)
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    meter_id: Mapped[UUID] = mapped_column(ForeignKey("meters.id"), nullable=False, index=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    previous_reading: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    current_reading: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    consumption: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    tariff_id: Mapped[UUID] = mapped_column(ForeignKey("utility_tariffs.id"), nullable=False)
    tariff_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
    calculated_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    source: Mapped[str] = mapped_column(String(20), nullable=False)
    import_batch_id: Mapped[UUID | None] = mapped_column(ForeignKey("utility_import_batches.id"))
    recorded_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BillModel(Base):
    __tablename__ = "bills"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    bill_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    contract_id: Mapped[UUID] = mapped_column(ForeignKey("contracts.id"), nullable=False, index=True)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    issued_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Draft", nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    adjustment_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    balance_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    issued_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    voided_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    voided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    void_reason: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class BillItemModel(Base):
    __tablename__ = "bill_items"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    bill_id: Mapped[UUID] = mapped_column(ForeignKey("bills.id"), nullable=False, index=True)
    item_type: Mapped[str] = mapped_column(String(30), nullable=False)
    reference_type: Mapped[str | None] = mapped_column(String(50))
    reference_id: Mapped[UUID | None] = mapped_column(Uuid)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    calculation_snapshot: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PaymentModel(Base):
    __tablename__ = "payments"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    bill_id: Mapped[UUID] = mapped_column(ForeignKey("bills.id"), nullable=False, index=True)
    payment_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    method: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Pending", nullable=False)
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    proof_file_id: Mapped[UUID | None] = mapped_column(ForeignKey("stored_files.id"))
    transaction_reference: Mapped[str | None] = mapped_column(String(100), unique=True)
    recorded_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reviewed_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[str | None] = mapped_column(String(500))
    receipt_no: Mapped[str | None] = mapped_column(String(50), unique=True)
    receipt_issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    receipt_issued_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    receipt_snapshot: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ViolationTypeModel(Base):
    __tablename__ = "violation_types"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000))
    default_fine_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ViolationModel(Base):
    __tablename__ = "violations"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    violation_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    contract_id: Mapped[UUID | None] = mapped_column(ForeignKey("contracts.id"))
    violation_type_id: Mapped[UUID] = mapped_column(ForeignKey("violation_types.id"), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[str | None] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    fine_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Recorded", nullable=False)
    recorded_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reviewed_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[str | None] = mapped_column(String(500))
    resolution_note: Mapped[str | None] = mapped_column(String(1000))
    bill_item_id: Mapped[UUID | None] = mapped_column(ForeignKey("bill_items.id"), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ViolationEvidenceModel(Base):
    __tablename__ = "violation_evidences"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    violation_id: Mapped[UUID] = mapped_column(ForeignKey("violations.id"), nullable=False, index=True)
    file_id: Mapped[UUID] = mapped_column(ForeignKey("stored_files.id"), nullable=False)
    description: Mapped[str | None] = mapped_column(String(300))
    uploaded_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MaintenanceRequestModel(Base):
    __tablename__ = "maintenance_requests"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    request_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    requester_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    building_id: Mapped[UUID | None] = mapped_column(ForeignKey("buildings.id"))
    room_id: Mapped[UUID | None] = mapped_column(ForeignKey("rooms.id"), index=True)
    bed_id: Mapped[UUID | None] = mapped_column(ForeignKey("beds.id"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="Submitted", nullable=False)
    assigned_to: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completion_note: Mapped[str | None] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class MaintenanceEventModel(Base):
    __tablename__ = "maintenance_events"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(ForeignKey("maintenance_requests.id"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(30), nullable=False)
    old_status: Mapped[str | None] = mapped_column(String(30))
    new_status: Mapped[str | None] = mapped_column(String(30))
    comment: Mapped[str | None] = mapped_column(String(2000))
    file_id: Mapped[UUID | None] = mapped_column(ForeignKey("stored_files.id"))
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MaintenancePlanModel(Base):
    __tablename__ = "maintenance_plans"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    building_id: Mapped[UUID | None] = mapped_column(ForeignKey("buildings.id"))
    room_id: Mapped[UUID | None] = mapped_column(ForeignKey("rooms.id"))
    bed_id: Mapped[UUID | None] = mapped_column(ForeignKey("beds.id"))
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    frequency_type: Mapped[str] = mapped_column(String(20), nullable=False)
    frequency_interval: Mapped[int] = mapped_column(Integer, nullable=False)
    next_due_date: Mapped[date] = mapped_column(Date, nullable=False)
    assigned_to: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class NotificationModel(Base):
    __tablename__ = "notifications"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Draft", nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="Normal", nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    published_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class NotificationTargetModel(Base):
    __tablename__ = "notification_targets"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    notification_id: Mapped[UUID] = mapped_column(ForeignKey("notifications.id"), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(20), nullable=False)
    role_id: Mapped[UUID | None] = mapped_column(ForeignKey("roles.id"))
    building_id: Mapped[UUID | None] = mapped_column(ForeignKey("buildings.id"))
    room_id: Mapped[UUID | None] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))


class NotificationReadModel(Base):
    __tablename__ = "notification_reads"
    notification_id: Mapped[UUID] = mapped_column(ForeignKey("notifications.id"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
