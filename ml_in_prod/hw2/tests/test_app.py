import pytest
import json

from fastapi.testclient import TestClient

from app import app, HeartDataModel, load_model


#client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def model_initialize():
    load_model()


@pytest.fixture()
def test_data():
    return [
        HeartDataModel(
            id=0, age=65, sex=1, cp=0, trestbps=138, chol=282, fbs=1, restecg=2,
            thalach=174, exang=0, oldpeak=1.4, slope=1, ca=1, thal=0
        ),
        HeartDataModel(
            id=1, age=69, sex=1, cp=0, trestbps=180, chol=204, fbs=0, restecg=0,
            thalach=162, exang=0, oldpeak=0.8, slope=0, ca=2, thal=0
        )
    ]


def test_read_main():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == 'Hi! I\'m Work!'


def test_health():
    with TestClient(app) as client:
        response = client.get("/health/")
        assert response.status_code == 200
        assert response.json() == True


def test_predict(test_data):
    with TestClient(app) as client:
        response = client.post(
            "/predict/", data=json.dumps([dict(x) for x in test_data])
        )
        assert response.status_code == 200
        assert response.json()[0]['condition'] in (0, 1)
        assert len(response.json()) == len(test_data)
