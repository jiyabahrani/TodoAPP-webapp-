from fastapi import status
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from ..main import app
from ..routers.todos import get_db, get_current_user
from ..database import Base
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
import pytest
from ..models import Todos

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'codingwithrobytest', 'id': 1, 'user_role': 'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

clint = TestClient(app)

# @pytest.fixture
# def test_todo():
#     todo = Todos(
#         title="learn to code!",
#         description="Need to learn everything!",
#         priority=5,
#         complete=False,
#         owner_id=1
#     )
#
#     db = TestingSessionLocal()
#     db.add(todo)
#     db.commit()
#     yield todo
#     with engine.connect() as connection:
#         connection.execute(text("DELETE FROM todos;"))
#         connection.commit()

def test_read_all_authenticated():
    response = clint.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

