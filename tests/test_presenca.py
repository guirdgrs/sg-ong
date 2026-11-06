import pytest
from datetime import date
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "SG-ONG — Diário de Classe Eletrônico" in response.text

def test_registrar_presenca_lote(client):
    payload = {
        "registros": [
            {
                "id_aluno": 101,
                "data_aula": str(date.today()),
                "status_presenca": "Presente",
                "id_educador": 1
            }
        ]
    }
    response = client.post("/presenca/lote", json=payload)
    assert response.status_code in [200, 201]