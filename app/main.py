from fastapi import FastAPI
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SG-ONG API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "API SG-ONG em execução com sucesso!"}