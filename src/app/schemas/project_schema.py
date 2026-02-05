import datetime
from pydantic import BaseModel, Field
from typing import Optional
from src.domain.entities.project import ProjectStatus

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None
    finalization_criteria: Optional[str] = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    budget: Optional[float] = Field(None, gt=0)


class ProjectResponse(BaseModel):
    id: int
    name: str
    status: ProjectStatus
    description: Optional[str] = None
    start_date: datetime.datetime
    end_date: Optional[datetime.datetime] = None
    finalization_criteria: Optional[str] = None
    budget: Optional[float] = None

    class Config:
        from_attributes = True # Esto permite que Pydantic lea la Entidad de Dominio