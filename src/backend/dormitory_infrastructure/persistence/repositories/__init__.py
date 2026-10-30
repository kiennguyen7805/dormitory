"""Stored-function repository implementations.

Application code imports repositories from this package. SQLAlchemy is used only
for connections, parameters and transactions; business reads/writes are delegated
to PostgreSQL functions installed from ``persistence/sql`` by Alembic.
"""

from .auth import AuthRepository, AuthUser, RoleRef
from .billing import StoredBillingRepository
from .contracts import StoredContractRepository
from .housing import StoredHousingRepository
from .identity import IdentityRepository
from .students import StudentRepository
from .utilities import StoredUtilityRepository

__all__ = [
    "AuthRepository",
    "AuthUser",
    "IdentityRepository",
    "RoleRef",
    "StoredBillingRepository",
    "StoredContractRepository",
    "StoredHousingRepository",
    "StoredUtilityRepository",
    "StudentRepository",
]
