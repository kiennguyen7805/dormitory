from .auth import router as auth_router
from .contracts import router as contracts_router
from .housing import router as housing_router

__all__ = ["auth_router", "contracts_router", "housing_router"]
