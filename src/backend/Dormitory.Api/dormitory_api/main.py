from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dormitory_api.controllers import auth_router, housing_router
from dormitory_api.middleware import register_error_handlers
from dormitory_infrastructure.persistence.config import get_settings

settings = get_settings()

app = FastAPI(title="Dormitory Management API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_error_handlers(app)
app.include_router(auth_router)
app.include_router(housing_router)


@app.get("/health", tags=["System"])
def health() -> dict[str, str]:
    return {"status": "ok"}
