from fastapi import APIRouter, HTTPException, status
from typing import List, Annotated
from src.app.services.project_service import ProjectService
from src.app.schemas.project_schema import ProjectCreate, ProjectResponse
from src.infrastructure.adapters.api.dependencies import get_project_service
from fastapi import Depends

# Definimos el router
router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

# Alias para la inyección del servicio, así el código queda más corto
ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_data: ProjectCreate, service: ProjectServiceDep):
    try:
        # El router extrae los datos del Schema y se los pasa al servicio
        return service.create_project(
            name=project_data.name, 
            description=project_data.description,
            start_date=project_data.start_date,
            end_date=project_data.end_date,
            finalization_criteria=project_data.finalization_criteria,
            status=project_data.status,
            budget=project_data.budget
        )
    except ValueError as e:
        import traceback
        traceback.print_exc()
        # Si el servicio lanza un error de negocio, lo convertimos en una respuesta HTTP con código 400
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ProjectResponse])
def list_projects(service: ProjectServiceDep):
    # El servicio devuelve Entidades de Dominio, 
    # pero FastAPI las convierte a ProjectResponse automáticamente
    return service.get_all_projects()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, service: ProjectServiceDep):
    project = service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectCreate, service: ProjectServiceDep):
    try:
        # Importamos la entidad para convertir el schema de entrada
        from src.domain.entities.project import Project
        
        # Creamos una entidad temporal con los nuevos datos
        project_entity = Project(
            name=project_data.name, 
            description=project_data.description
        )
        
        updated = service.update_project(project_id, project_entity)
        if not updated:
            raise HTTPException(status_code=404, detail="Project not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, service: ProjectServiceDep):
    deleted = service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return None  # FastAPI interpretará esto como una respuesta vacía con código 204