from typing import List, Optional
from src.domain.entities.task import Task, TaskStatus
from src.domain.repositories.task_repository import TaskRepository
from src.domain.repositories.epic_repository import EpicRepository

class TaskService:
    def __init__(self, task_repository: TaskRepository, epic_repository: EpicRepository):
        # Inyectamos la interfaz (Puerto), no la implementación
        self.task_repository = task_repository
        self.epic_repository = epic_repository

    def create_task(self, name: str, epic_id: int, description: Optional[str] = None) -> Task:
        # --- REGLA DE NEGOCIO 1: Verificar que la épica exista ---
        epic = self.epic_repository.get_by_id(epic_id)
        if not epic:
            raise ValueError(f"The epic with ID {epic_id} does not exist.")

        # --- REGLA DE NEGOCIO 2: No nombres duplicados dentro de la misma épica ---
        existing_tasks = self.task_repository.get_by_epic_id(epic_id)
        if any(t.name.lower() == name.lower() for t in existing_tasks):
            raise ValueError(f"The task with name '{name}' already exists in epic ID {epic_id}.")

        # Creamos la entidad y la mandamos al "puerto"
        new_task = Task(name=name, epic_id=epic_id, description=description)
        return self.task_repository.add(new_task)
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return self.task_repository.get_by_id(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        return self.task_repository.get_all()
    
    def update_task(self, task: Task, task_id: int) -> Task:
        
        # --- REGLA DE NEGOCIO 3: Verificar que la tarea exista ---
        existing_task = self.get_task_by_id(task_id)
        if not existing_task:
            raise ValueError(f"The task with ID {task_id} does not exist.")
        
        # --- REGLA DE NEGOCIO 4: No actualizar si el nombre ya existe (excepto para la misma tarea) ---
        existing_tasks = self.task_repository.get_by_epic_id(existing_task.epic_id)
        for t in existing_tasks:
            if t.name.lower() == task.name.lower() and t.id != task_id:
                raise ValueError(f"The task with name '{task.name}' already exists in epic ID {existing_task.epic_id}.")
        
        # --- REGLA DE NEGOCIO 5: No actualizar si la tarea está COMPLETED, solo el estado ---
        if existing_task.status == TaskStatus.DONE:
            if task.name != existing_task.name or task.description != existing_task.description or task.finalization_date != existing_task.finalization_date or \
               task.finalization_criteria != existing_task.finalization_criteria or task.epic_id != existing_task.epic_id:
                raise ValueError(f"The task with ID {task_id} cannot be updated because its status is DONE.")
        
        # Actualizamos la tarea
        task.id = task_id
        return self.task_repository.update(task)
    
    def delete_task(self, task_id: int):
        # --- REGLA DE NEGOCIO 6: Verificar que la tarea exista antes de eliminar ---
        existing_task = self.get_task_by_id(task_id)
        if not existing_task:
            raise ValueError(f"The task with ID {task_id} does not exist.")
        
        # --- REGLA DE NEGOCIO 7: No eliminar si la tarea está COMPLETED ---
        if existing_task.status == TaskStatus.DONE:
            raise ValueError(f"The task with ID {task_id} cannot be deleted because its status is DONE.")

        return self.task_repository.delete(task_id)
    
    def get_tasks_by_epic_id(self, epic_id: int) -> List[Task]:
        #  --- REGLA DE NEGOCIO 8: Verificar que la épica exista ---
        epic = self.epic_repository.get_by_id(epic_id)
        if not epic:
            raise ValueError(f"The epic with ID {epic_id} does not exist.")
        
        return self.task_repository.get_by_epic_id(epic_id)
    
    def get_count_tasks_by_epic_id(self, epic_id: int) -> int:
        #  --- REGLA DE NEGOCIO 9: Verificar que la épica exista ---
        epic = self.epic_repository.get_by_id(epic_id)
        if not epic:
            raise ValueError(f"The epic with ID {epic_id} does not exist.")
        
        return self.task_repository.get_count_by_epic_id(epic_id)