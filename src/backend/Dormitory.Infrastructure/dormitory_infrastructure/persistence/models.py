from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    users: Mapped[list["UserModel"]] = relationship(back_populates="role")


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped[RoleModel] = relationship(back_populates="users")


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str] = mapped_column(String(250), default="", nullable=False)
    floors: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    rooms: Mapped[list["RoomModel"]] = relationship(
        back_populates="building", cascade="all, delete-orphan"
    )


class RoomTypeModel(Base):
    __tablename__ = "room_types"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    default_monthly_rate: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    rooms: Mapped[list["RoomModel"]] = relationship(back_populates="room_type")


class RoomModel(Base):
    __tablename__ = "rooms"
    __table_args__ = (UniqueConstraint("building_id", "code", name="uq_rooms_building_code"),)

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    building_id: Mapped[UUID] = mapped_column(ForeignKey("buildings.id"), nullable=False)
    room_type_id: Mapped[UUID] = mapped_column(ForeignKey("room_types.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
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
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Submitted", index=True
    )
    rejection_reason: Mapped[str | None] = mapped_column(String(500))
    reviewed_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
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
    terminated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    student: Mapped[UserModel] = relationship()
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
    contract: Mapped[ContractModel] = relationship(back_populates="assignments")
    bed: Mapped[BedModel] = relationship(back_populates="assignments")
