from app.database import Base
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id_aluno = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_completo = Column(String(150), nullable=False)
    matricula = Column(String(20), unique=True, nullable=False, index=True)
    polo_atendimento = Column(String(50), nullable=False)
    status_matricula = Column(String(20), default="Ativo", nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento 1:N (Um aluno possui vários registros de presença)
    presencas = relationship("RegistroPresenca", back_populates="aluno")


class RegistroPresenca(Base):
    __tablename__ = "registros_presenca"

    id_presenca = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), nullable=False)
    data_aula = Column(Date, nullable=False)
    status_presenca = Column(String(20), nullable=False) # 'Presente', 'Ausente', 'Justificado'
    id_educador = Column(Integer, nullable=False)
    data_registro = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento N:1
    aluno = relationship("Aluno", back_populates="presencas")

    # Restrição de unicidade composta: impede registrar duas chamadas para o mesmo aluno na mesma data
    __table_args__ = (
        UniqueConstraint('id_aluno', 'data_aula', name='uq_aluno_data_aula'),
    )