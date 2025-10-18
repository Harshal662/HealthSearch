from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)
HEADERS = {"Authorization": f"Bearer {settings.HEALTHSEARCH_TOKEN}"}

def test_add_and_search_single_note():
    # add two notes
    r1 = client.post("/add_note", json={"patient_id":"P001","note":"Patient has fever and cough."}, headers=HEADERS)
    assert r1.status_code == 200
    r2 = client.post("/add_note", json={"patient_id":"P002","note":"No fever, happy and healthy."}, headers=HEADERS)
    assert r2.status_code == 200

    # search for fever
    r = client.get("/search_notes?q=fever", headers=HEADERS)
    assert r.status_code == 200
    body = r.json()
    assert body["query"] == "fever"
    assert len(body["results"]) >= 1
    # top result should be P001 or at least high similarity
    assert any(res["patient_id"] == "P001" for res in body["results"])

def test_auth_missing():
    r = client.post("/add_note", json={"patient_id":"P003","note":"something"})
    assert r.status_code == 401
