from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, UniqueConstraint, Uuid
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
