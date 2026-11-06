import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os

# Na Vercel, usa o diretório temporário /tmp/ para o banco SQLite
IF_VERCEL = os.environ.get("VERCEL")

if IF_VERCEL:
    SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/sql_app.db"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Utiliza SQLite local se DATABASE_URL não estiver definida
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sg_ong.db")

# Para SQLite, é necessário o check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()