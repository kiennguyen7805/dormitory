from enum import StrEnum


class RoleName(StrEnum):
    ADMIN = "Admin"
    STAFF = "Staff"
    STUDENT = "Student"


class BedStatus(StrEnum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"
