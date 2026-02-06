import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.repositories.task_repository import TaskRepository
from src.domain.entities.task import Task, TaskStatus, TaskPriority
from src.infrastructure.models import TaskModel

class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: Session):
        self.db = db
    
    # funcion privada para convertir de modelo de DB a entidad de Dominio y evitar repetición de código y errores de Pylance
    def _to_entity(self, db_model: TaskModel) -> Task:
        return Task(
            # Usamos variables intermedias si Pylance sigue quejándose
            # o simplemente nos aseguramos de que no sean nulos donde no deben
            epic_id=int(db_model.epic_id), # type: ignore
            name=str(db_model.name), # type: ignore
            id=int(db_model.id) if db_model.id is not None else None, # type: ignore
            description=str(db_model.description) if db_model.description else None, # type: ignore
            created_at=db_model.created_at if db_model.created_at else datetime.datetime.now(), # type: ignore
            updated_at=datetime.datetime.now() if db_model.updated_at is None else db_model.updated_at, # type: ignore
            target_date=db_model.target_date if db_model.target_date else None, # type: ignore
            finalization_criteria=db_model.finalization_criteria if db_model.finalization_criteria else None, # type: ignore
            finalization_date=db_model.finalization_date if db_model.finalization_date else None, # type: ignore
            status=TaskStatus(db_model.status) if db_model.status else None, # type: ignore
            assignee=db_model.assignee if db_model.assignee else None, # type: ignore
            priority=TaskPriority(db_model.priority) if db_model.priority else None, # type: ignore
        )

    def add(self, task: Task) -> Task:
        # 1. Convertimos la Entidad de Dominio en un Modelo de DB
        db_task = TaskModel(
            epic_id=task.epic_id,
            name=task.name,
            description=task.description,
            created_at=task.created_at,
            updated_at=task.updated_at,
            target_date=task.target_date,
            finalization_criteria=task.finalization_criteria,
            finalization_date=task.finalization_date,
            status=task.status.value,
            assignee=task.assignee,
            priority=task.priority.value
        )
        # 2. Guardamos en MySQL
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task) # Para obtener el ID generado automáticamente
        
        # 3. Devolvemos el objeto actualizado con su ID
        task.id = db_task.id if isinstance(db_task.id, int) else None
        return self._to_entity(db_task)
    
    def update(self, task_id:int, task: Task) -> Optional[Task]:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            raise ValueError("Task not found")
        
        #Actualizamos los campos en los que se ha escrito alguna información
        #Usamos ignore para evitar errores marcados por Pylance por la duda de tipos en el metacodigo de sqlalchemy
        
        if task.name is not None:
            db_task.name = task.name # type: ignore
            
        if task.description is not None:
            db_task.description = task.description # type: ignore
            
        if task.target_date is not None:
            db_task.target_date = task.target_date # type: ignore
        
        if task.finalization_criteria is not None:
            db_task.finalization_criteria = task.finalization_criteria # type: ignore

        if task.finalization_date is not None:
            db_task.finalization_date = task.finalization_date # type: ignore
        
        if task.status is not None:
            db_task.status = task.status.value  # type: ignore

        if task.assignee is not None:
            db_task.assignee = task.assignee  # type: ignore

        if task.priority is not None:
            db_task.priority = task.priority.value  # type: ignore
        
        db_task.updated_at = datetime.datetime.now()  # type: ignore
        
        self.db.commit()
        self.db.refresh(db_task)
        
        return self._to_entity(db_task)
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            raise ValueError("Task not found")
        
        return self._to_entity(db_task)
    
    def get_all(self) -> Optional[List[Task]]:
        db_tasks = self.db.query(TaskModel).all()
        if not db_tasks:
            raise ValueError("No tasks found")
        
        #Retornamos una lista de db_tasks como hemos tipado en la función
        return [self._to_entity(db_task) for db_task in db_tasks]
    
    def get_by_epic_id(self, epic_id: int) -> Optional[List[Task]]:
        db_tasks = self.db.query(TaskModel).filter(TaskModel.epic_id == epic_id).all()
        if not epic_id:
            raise ValueError("Epic ID must be provided")
        if not db_tasks:
            raise ValueError("No tasks found for the given epic ID")
        return [self._to_entity(db_task) for db_task in db_tasks]
    
    def delete(self, task_id: int) -> bool:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            raise ValueError("Task not found")
        
        self.db.delete(db_task)
        self.db.commit()
        return True

    def get_count_by_epic_id(self, epic_id: int) -> int:
        count = self.db.query(TaskModel).filter(TaskModel.epic_id == epic_id).count()
        return count