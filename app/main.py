from fastapi import FastAPI
from app.database import engine, Base
from app.api import presenca

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SG-ONG API", version="1.0.0")

# Inclui as rotas de presença
app.include_router(presenca.router)

@app.get("/")
def read_root():
    return {"message": "API SG-ONG em execução com sucesso!"}