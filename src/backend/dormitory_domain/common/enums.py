from enum import StrEnum


class RoleName(StrEnum):
    ADMIN = "Admin"
    STAFF = "Staff"
    STUDENT = "Student"


class BedStatus(StrEnum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"


class HousingApplicationStatus(StrEnum):
    SUBMITTED = "Submitted"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class ContractStatus(StrEnum):
    ACTIVE = "Active"
    TERMINATED = "Terminated"


class BedAssignmentStatus(StrEnum):
    ACTIVE = "Active"
    ENDED = "Ended"
