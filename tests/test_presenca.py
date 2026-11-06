from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Valida se a rota principal responde com status 200"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API SG-ONG em execução com sucesso!"}

def test_registrar_chamada_lote():
    """Valida o registro de presença em lote na API"""
    payload = {
        "polo_atendimento": "Polo Centro",
        "turma": "Turma A",
        "data_aula": "2026-11-05",
        "id_educador": 1,
        "registros": [
            {
                "id_aluno": 101,
                "data_aula": "2026-11-05",
                "status_presenca": "Presente",
                "id_educador": 1
            }
        ]
    }

def test_registrar_presenca_lote(client):
    payload = {
        "registros": [
            {
                "id_aluno": 101,
                "data_aula": "2026-11-05",
                "status_presenca": "Presente",
                "id_educador": 1
            }
        ]
    }
    response = client.post("/presenca/lote", json=payload)
    assert response.status_code in [200, 201]