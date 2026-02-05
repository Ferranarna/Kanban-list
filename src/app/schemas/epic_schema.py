import datetime
from pydantic import BaseModel, Field
from typing import Optional
from src.domain.entities.epic import EpicStatus, EpicPriority

class EpicCreate(BaseModel):
    project_id: int
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    start_date: Optional[datetime.datetime] = None #Se añade datetime.datetime para evitar confusiones con el tipo datetime del dominio
    end_date: Optional[datetime.datetime] = None
    completion_criteria: Optional[str] = None
    status: EpicStatus = EpicStatus.NOT_STARTED
    priority: EpicPriority = EpicPriority.LOW


class EpicResponse(BaseModel):
    id: int
    project_id: int
    name: str 
    description: Optional[str] = None
    start_date: Optional[datetime.datetime] = None #Se añade datetime.datetime para evitar confusiones con el tipo datetime del dominio
    end_date: Optional[datetime.datetime] = None
    completion_criteria: Optional[str] = None
    status: EpicStatus = EpicStatus.NOT_STARTED
    priority: EpicPriority = EpicPriority.LOW

    class Config:
        from_attributes = True # Esto permite que Pydantic lea la Entidad de Dominio