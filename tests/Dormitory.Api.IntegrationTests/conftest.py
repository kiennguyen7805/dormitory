from collections.abc import Generator
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from dormitory_api.main import app
from dormitory_infrastructure.identity.seeder import seed_identity
from dormitory_infrastructure.persistence import Base, get_db
from dormitory_infrastructure.persistence import models  # noqa: F401


@pytest.fixture()
def client(tmp_path) -> Generator[TestClient, None, None]:
    test_database_url = os.getenv("TEST_DATABASE_URL")
    if test_database_url:
        engine = create_engine(test_database_url, pool_pre_ping=True)
        Base.metadata.drop_all(engine)
    else:
        database_path = tmp_path / "test.db"
        engine = create_engine(
            f"sqlite:///{database_path}",
            connect_args={"check_same_thread": False},
        )
    testing_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(engine)

    with testing_session() as session:
        seed_identity(session)

    def override_get_db() -> Generator[Session, None, None]:
        with testing_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    if test_database_url:
        Base.metadata.drop_all(engine)
    engine.dispose()
