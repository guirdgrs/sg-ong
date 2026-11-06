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
        # Trata conversão de string para objeto date se necessário
        data_valida = item.data_aula
        if isinstance(data_valida, str):
            try:
                data_valida = datetime.strptime(item.data_aula, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Formato de data inválido para o aluno {item.id_aluno}. Use YYYY-MM-DD."
                )
        
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

@router.get("/alunos", response_model=List[dict])
def listar_alunos(db: Session = Depends(get_db)):
    """Retorna os alunos cadastrados no banco para renderização da chamada."""
    alunos = db.query(Aluno).all()
    return [
        {
            "id_aluno": a.id_aluno, 
            "matricula": a.matricula, 
            "nome": a.nome, 
            "polo": a.polo, 
            "turma": a.turma
        } for a in alunos
    ]