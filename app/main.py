from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.models import Aluno
from app.api import presenca
from mangum import Mangum

# Cria as tabelas na nova base de dados SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SG-ONG API", version="1.0.0")
templates = Jinja2Templates(directory="app/templates")

app.include_router(presenca.router)

def popular_banco_se_vazio(db: Session):
    if db.query(Aluno).count() == 0:
        alunos_iniciais = [
            Aluno(id_aluno=101, matricula="2026001", nome_aluno="Ana Souza", polo="Polo Centro", turma="Turma A — Informática"),
            Aluno(id_aluno=102, matricula="2026002", nome_aluno="Carlos Eduardo", polo="Polo Centro", turma="Turma A — Informática"),
            Aluno(id_aluno=103, matricula="2026003", nome_aluno="Bruno Lima", polo="Polo Centro", turma="Turma A — Informática"),
        ]
        db.add_all(alunos_iniciais)
        db.commit()

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    """Renderiza a interface web com dados vindos da base de dados SQLite"""
    popular_banco_se_vazio(db)
    alunos = db.query(Aluno).all()
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"alunos": alunos}
    )

handler = Mangum(app)