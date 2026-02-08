from fastapi import APIRouter, HTTPException, status
from typing import List, Annotated
from src.app.services.task_service import TaskService
from src.app.schemas.task_schema import TaskCreate, TaskResponse
from src.infrastructure.adapters.api.dependencies import get_task_service
from fastapi import Depends

# Definimos el router
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# Alias para la inyección del servicio, así el código queda más corto
TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, service: TaskServiceDep):
    try:
        # El router extrae los datos del Schema y se los pasa al servicio
        return service.create_task(
            name=task_data.name, 
            description=task_data.description,
            epic_id=task_data.epic_id
        )
    except ValueError as e:
        # Si el servicio lanza un error de negocio, lo convertimos en una respuesta HTTP con código 400
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TaskResponse])
def list_tasks(service: TaskServiceDep):
    # El servicio devuelve Entidades de Dominio, 
    # pero FastAPI las convierte a TaskResponse automáticamente
    return service.get_all_tasks()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, service: TaskServiceDep):
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@router.get("/epic-tasks/{epic_id}", response_model=List[TaskResponse])
def get_tasks_by_epic(epic_id: int, service: TaskServiceDep):
    return service.get_tasks_by_epic_id(epic_id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskCreate, service: TaskServiceDep):
    try:
        # Importamos la entidad para convertir el schema de entrada
        from src.domain.entities.task import Task
        
        # Creamos una entidad temporal con los nuevos datos
        task_entity = Task(
            name=task_data.name, 
            description=task_data.description,
            epic_id=task_data.epic_id
        )
        
        updated = service.update_task(task_entity, task_id)
        if not updated:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, service: TaskServiceDep):
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None  # FastAPI interpretará esto como una respuesta vacía con código 204

@router.get("/count/{epic_id}", response_model=int)
def count_tasks_by_epic(epic_id: int, service: TaskServiceDep):
    return service.get_count_tasks_by_epic_id(epic_id)