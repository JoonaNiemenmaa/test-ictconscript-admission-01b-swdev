import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from backend import app, get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={ "check_same_thread": False }, poolclass=StaticPool)
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


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert(response.status_code == 200)
    assert(response.text == "\"OK\"")

def test_post_entry_bad(client: TestClient):
    case = {
        "title": "Night perimeter check",
        "lat": "this is not right",
        "lon": 25.0293
    }
    response = client.post("/entries", json=case)

    assert(response.status_code == 422)

    assert response.json() == {
        "detail": [
            {
                "input": {
                    "lat": "this is not right",
                    "lon": 25.0293,
                    "title": "Night perimeter check"
                },
                "loc": [
                    "body",
                    "body"
                ],
                "msg": "Field required",
                "type": "missing"
            },
            {
                "input": "this is not right",
                "loc": [
                    "body",
                    "lat"
                ],
                "msg": "Input should be a valid number, unable to parse string as a number",
                "type": "float_parsing"
            }
        ]
    }

def test_post_entry_happy(client: TestClient):
    case = {
        "title": "Night perimeter check",
        "body": "All clear around main gate.",
        "lat": 60.1503,
        "lon": 25.0293
    }
    response = client.post("/entries", json=case)

    assert(response.status_code == 201)

    json = response.json()

    assert json["title"] == case["title"]
    assert json["body"] == case["body"]
    assert json["lat"] == case["lat"]
    assert json["lon"] == case["lon"]

def test_get(client: TestClient):
    response = client.post("/entries", json = {
        "title": "Night perimeter check",
        "body": "All clear around main gate.",
        "lat": 60.1503,
        "lon": 25.0293
    })

    entry = response.json()

    assert response.status_code == 201

    response = client.get("/entries")

    assert response.status_code == 200
    assert response.json() == [entry]
