from pydantic import BaseModel
from datetime import date
from typing import List, Union, Optional

class PresencaCreate(BaseModel):
    id_aluno: int
    data_aula: Union[date, str]
    status_presenca: str
    id_educador: Optional[int] = 1

    class Config:
        from_attributes = True

class ChamadaLoteCreate(BaseModel):
    registros: List[PresencaCreate]

class PresencaResponse(BaseModel):
    id_presenca: Optional[int] = None
    id_aluno: int
    data_aula: Union[date, str]
    status_presenca: str
    id_educador: Optional[int] = 1

    class Config:
        from_attributes = True