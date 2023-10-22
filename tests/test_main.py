from fastapi.testclient import TestClient

from sopros_osa_backend.main import app
from sopros_osa_backend.model import State
from sopros_osa_backend.model import SOPROSCountry


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_country():
    with TestClient(app) as client:
        response = client.get("/country")
        assert response.status_code == 200
        print (response.json())
        country = SOPROSCountry(**(response.json()["ger"]))
        assert country.states[0].id == "MIL"

def test_read_states():
    with TestClient(app) as client:
        response = client.get("/states/ger")
        print(response)
        assert response.status_code == 200
        item_json = response.json()[0]
        item = State(**item_json)
        assert item.id == "MIL"