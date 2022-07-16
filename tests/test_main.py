import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from ToDoListApp.app.main import app, get_session
from ToDoListApp.app.models import ToDoListItem


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_item(client: TestClient):
    response = client.post(
        "/items/", json={"description": "test item", "owner": "test user",
        "deadline": "2022-07-20", "progress": "In progress"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["description"] == "test item"
    assert data["owner"] == "test user"
    assert data["priority"] is None
    assert data["team_id"] is None
    assert data["id"] is not None
