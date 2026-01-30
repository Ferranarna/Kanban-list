from sqlalchemy import Column, Integer, String, DateTime, Float, Enum as SQLEnum, ForeignKey
from src.domain.entities.task import TaskStatus, TaskPriority
from src.domain.entities.epic import EpicStatus, EpicPriority
from src.infrastructure.database import Base
from src.domain.entities.project import ProjectStatus
import datetime

class ProjectModel(Base):
    __tablename__ = "projects"

    # Detalles técnicos que el Dominio no necesita saber
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    finalization_criteria = Column(String(500), nullable=True)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.ACTIVE)
    budget = Column(Float, nullable=True)
    
    # Fechas automáticas gestionadas por la base de datos
    start_date = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    end_date = Column(DateTime, nullable=True)

class EpicModel(Base):
    __tablename__ = "epics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    completion_criteria = Column(String(500), nullable=True)
    status = Column(SQLEnum(EpicStatus), default=EpicStatus.NOT_STARTED)
    priority = Column(SQLEnum(EpicPriority), default=EpicPriority.LOW)
    
    # Fechas automáticas gestionadas por la base de datos
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    epic_id = Column(Integer, ForeignKey("epics.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    finalization_criteria = Column(String(500), nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TO_DO)
    assignee = Column(String(100), nullable=True)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.LOW)
    
    # Fechas automáticas gestionadas por la base de datos
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    target_date = Column(DateTime, nullable=True)
    finalization_date = Column(DateTime, nullable=True)
    
    
