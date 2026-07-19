import datetime

from fastapi.testclient import TestClient
from backend import app

test_client = TestClient(app)

def test_health_check():
    response = test_client.get("/health")
    assert(response.status_code == 200)
    assert(response.text == "\"OK\"")

def test_post_entry():
    response = test_client.post("/entries", json={
        "title": "Night perimeter check",
        "body": "All clear around main gate.",
        "lat": 60.1503,
        "lon": 25.0293
    })

    assert(response.status_code == 201)
    assert response.json() == {
        "id": 1,
        "title": "Night perimeter check",
        "body": "All clear around main gate.",
        "iso_time": datetime.datetime.now().replace(microsecond=0).isoformat(),
        "lat": 60.1503,
        "lon": 25.0293
    }
