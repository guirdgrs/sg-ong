from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List

from app.database import get_db
from app.models import Presenca
from app.schemas import ChamadaLoteCreate, PresencaResponse

router = APIRouter(prefix="/presenca", tags=["Presença"])

@router.post("/lote", response_model=List[PresencaResponse], status_code=status.HTTP_201_CREATED)
def registrar_presenca_lote(dados: ChamadaLoteCreate, db: Session = Depends(get_db)):
    novos_registros = []
    
    for item in dados.registros:
        data_valida = item.data_aula
        if isinstance(data_valida, str):
            try:
                data_valida = datetime.strptime(item.data_aula, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Formato de data inválido para o aluno {item.id_aluno}."
                )
        
        # Busca registro existente para evitar erro de UNIQUE constraint
        presenca_existente = db.query(Presenca).filter(
            Presenca.id_aluno == item.id_aluno,
            Presenca.data_aula == data_valida
        ).first()

        if presenca_existente:
            # Atualiza o status existente
            presenca_existente.status_presenca = item.status_presenca
            presenca_existente.id_educador = item.id_educador or 1
            novos_registros.append(presenca_existente)
        else:
            # Cria novo registro
            presenca_obj = Presenca(
                id_aluno=item.id_aluno,
                data_aula=data_valida,
                status_presenca=item.status_presenca,
                id_educador=item.id_educador or 1
            )
            db.add(presenca_obj)
            novos_registros.append(presenca_obj)
    
    db.commit()
    for reg in novos_registros:
        db.refresh(reg)
        
    return novos_registros