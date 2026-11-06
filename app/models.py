from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id_aluno = Column(Integer, primary_key=True, index=True)
    matricula = Column(String, unique=True, index=True)
    nome_aluno = Column(String, nullable=False)
    polo = Column(String, nullable=True)
    turma = Column(String, nullable=True)

    # Relação apontando para o nome correto da classe: Presenca
    presencas = relationship("Presenca", back_populates="aluno")


class Presenca(Base):
    __tablename__ = "presencas"

    id_presenca = Column(Integer, primary_key=True, index=True)
    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), nullable=False)
    data_aula = Column(Date, nullable=False)
    status_presenca = Column(String, nullable=False)
    id_educador = Column(Integer, nullable=True, default=1)

    # Relação inversa apontando para Aluno
    aluno = relationship("Aluno", back_populates="presencas")