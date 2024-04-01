from fastapi.testclient import TestClient

from sopros_osa_backend.main import app
from sopros_osa_backend.model import SoprosCountry
from sopros_osa_backend.model import SoprosRule
from sopros_osa_backend.model import SoprosStatus


client = TestClient(app)


def test_read_main():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_country():
    with TestClient(app) as client:
        response = client.get("/api/country/GER")
        assert response.status_code == 200
        print (response.json())
        country = SoprosCountry(**(response.json()))
        assert country.id == "GER"
        assert country.questions != []
        assert country.questions_athlete != []
        assert country.rules != []

def test_read_states():
    with TestClient(app) as client:
        response = client.get("/api/status")
        print(response)
        assert response.status_code == 200
        items_json = response.json()
        status_list = [SoprosStatus(**item) for item in items_json]
        assert status_list != []
        assert any(item.id == "MIL" for item in status_list) == True

def test_calc_success_GER_CIT():
    with TestClient(app) as client:
        response = client.post("/api/calc/GER", content='["CIT"]')
        print(response)
        assert response.status_code == 200
        items_json = response.json()
        rule_list = [SoprosRule(**item) for item in items_json]
        assert len(items_json) == 10
        assert any(item.id == "MAT_MINCOV_CIT" for item in rule_list) == True

def test_calc_success_invalidates_GER_CIT_MIL():
    with TestClient(app) as client:
        response = client.post("/api/calc/GER", content='["CIT", "MIL"]')
        print(response)
        assert response.status_code == 200
        items_json = response.json()
        rule_list = [SoprosRule(**item) for item in items_json]
        assert len(items_json) == 25
        assert any(item.id == "MAT_MINCOV_CIT" for item in rule_list) == False