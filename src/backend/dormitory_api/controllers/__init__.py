from .auth import router as auth_router
from .billing import router as billing_router
from .contracts import router as contracts_router
from .housing import router as housing_router
from .identity import router as identity_router
from .students import router as students_router
from .utilities import router as utilities_router

__all__ = [
    "auth_router",
    "billing_router",
    "contracts_router",
    "housing_router",
    "identity_router",
    "students_router",
    "utilities_router",
]
