import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["CRM_BASE_URL"] = "http://localhost:9000"
os.environ["CRM_API_KEY"] = "dev-crm-key"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@pytest.fixture
def client():
    def override_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
