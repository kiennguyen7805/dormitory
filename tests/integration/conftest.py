"""API integration tests run against a dedicated PostgreSQL database.

Set TEST_DATABASE_URL to a separate test database. The fixture never touches the
application database and deliberately has no SQLite/ORM fallback.
"""

from collections.abc import Generator
import os
from pathlib import Path

from alembic import command
from alembic.config import Config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, make_url

from dormitory_api.main import app
from dormitory_infrastructure.identity.seeder import seed_identity
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.config import get_settings


BACKEND = Path(__file__).resolve().parents[2] / "src" / "backend"


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("API integration tests require a dedicated PostgreSQL TEST_DATABASE_URL")
    if make_url(url).get_backend_name() != "postgresql":
        pytest.skip("API integration tests require PostgreSQL stored functions")
    if make_url(url) == make_url(get_settings().database_url):
        pytest.fail("TEST_DATABASE_URL must not point to the application database")

    config = Config(str(BACKEND / "alembic.ini"))
    config.set_main_option(
        "script_location",
        str(BACKEND / "dormitory_infrastructure" / "persistence" / "migrations"),
    )
    config.attributes["database_url"] = url
    command.upgrade(config, "head")

    engine = create_engine(url, pool_pre_ping=True)
    with engine.begin() as connection:
        tables = connection.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public' "
                 "AND tablename <> 'alembic_version' ORDER BY tablename")
        ).scalars().all()
        if len(tables) != 16:
            pytest.fail(f"Expected 16 application tables in test database; found {len(tables)}")
        # Names come only from PostgreSQL's own catalog, not user input.
        quoted = ", ".join('"' + name.replace('"', '""') + '"' for name in tables)
        connection.exec_driver_sql(f"TRUNCATE TABLE {quoted} RESTART IDENTITY CASCADE")

    with engine.connect() as connection:
        seed_identity(connection)

    def override_get_db() -> Generator[Connection, None, None]:
        with engine.connect() as connection:
            yield connection

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
