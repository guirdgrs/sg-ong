from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.models import RegistroPresenca, Aluno
from app.schemas import PresencaCreate, PresencaResponse, ChamadaLoteCreate
from app.services.pdf_service import gerar_relatorio_presenca_pdf

# Instancia o router da API de presenças (com o prefixo /presenca)
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


@router.get("/relatorio/pdf")
def baixar_relatorio_pdf(polo: str = "Polo Centro", turma: str = "Turma A", data_aula: str = "2026-11-05", db: Session = Depends(get_db)):
    """
    Rota para gerar e transferir o relatório de assiduidade formatado em PDF (RF03).
    """
    registros_demo = [
        {"matricula": "2026001", "nome_aluno": "Ana Souza", "status_presenca": "Presente"},
        {"matricula": "2026002", "nome_aluno": "Carlos Eduardo", "status_presenca": "Justificado"},
        {"matricula": "2026003", "nome_aluno": "Bruno Lima", "status_presenca": "Ausente"},
    ]
    
    pdf_content = gerar_relatorio_presenca_pdf(polo, turma, date.fromisoformat(data_aula), registros_demo)
    
    headers = {
        "Content-Disposition": f"attachment; filename=Relatorio_Assiduidade_{turma}.pdf"
    }
    return Response(content=pdf_content, media_type="application/pdf", headers=headers)