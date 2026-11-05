from fastapi import Response
from app.services.pdf_service import gerar_relatorio_presenca_pdf

@router.get("/relatorio/pdf")
def baixar_relatorio_pdf(polo: str = "Polo Centro", turma: str = "Turma A", data_aula: str = "2026-11-05", db: Session = Depends(get_db)):
    """
    Rota para gerar e transferir o relatório de assiduidade formatado em PDF (RF03).
    """
    # Consulta registros fictícios/locais para a demonstração
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