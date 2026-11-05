from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import List, Optional

# Schemas de Registro de Presença
BaseModel
class PresencaCreate(BaseModel):
    id_aluno: int
    data_aula: date
    status_presenca: str  # 'Presente', 'Ausente', 'Justificado'
    id_educador: int

class PresencaResponse(PresencaCreate):
    id_presenca: int
    data_registro: datetime

    model_config = ConfigDict(from_attributes=True)

# Schema para recebimento de chamada em lote (PWA / Offline Sync)
class ChamadaLoteCreate(BaseModel):
    polo_atendimento: str
    turma: str
    data_aula: date
    id_educador: int
    registros: List[PresencaCreate]