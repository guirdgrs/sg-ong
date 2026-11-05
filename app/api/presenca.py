from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import RegistroPresenca, Aluno
from app.schemas import PresencaCreate, PresencaResponse, ChamadaLoteCreate

router = APIRouter(prefix="/presenca", tags=["Presenças"])

@router.post("/lote", response_model=List[PresencaResponse], status_code=status.HTTP_201_CREATED)
def registrar_chamada_lote(dados_chamada: ChamadaLoteCreate, db: Session = Depends(get_db)):
    """
    Registra a chamada de uma turma em lote.
    Suporta envios em massa gerados pela sincronização offline do PWA.
    """
    novos_registros = []
    
    for item in dados_chamada.registros:
        # Verifica se já existe chamada gravada para o aluno na mesma data
        existente = db.query(RegistroPresenca).filter(
            RegistroPresenca.id_aluno == item.id_aluno,
            RegistroPresenca.data_aula == item.data_aula
        ).first()

        if existente:
            # Atualiza o status se já existir registro prévio
            existente.status_presenca = item.status_presenca
            existente.id_educador = item.id_educador
            novos_registros.append(existente)
        else:
            # Cria novo registro
            novo = RegistroPresenca(
                id_aluno=item.id_aluno,
                data_aula=item.data_aula,
                status_presenca=item.status_presenca,
                id_educador=item.id_educador
            )
            db.add(novo)
            novos_registros.append(novo)

    db.commit()
    for reg in novos_registros:
        db.refresh(reg)

    return novos_registros