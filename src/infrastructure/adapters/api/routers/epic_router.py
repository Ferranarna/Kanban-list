from fastapi import APIRouter, HTTPException, status
from typing import List, Annotated
from src.app.services.epic_service import EpicService
from src.app.schemas.epic_schema import EpicCreate, EpicResponse
from src.infrastructure.adapters.api.dependencies import get_epic_service
from fastapi import Depends

# Definimos el router
router = APIRouter(
    prefix="/epics",
    tags=["Epics"]
)

# Alias para la inyección del servicio, así el código queda más corto
EpicServiceDep = Annotated[EpicService, Depends(get_epic_service)]

@router.post("/", response_model=EpicResponse, status_code=status.HTTP_201_CREATED)
def create_epic(epic_data: EpicCreate, service: EpicServiceDep):
    try:
        # El router extrae los datos del Schema y se los pasa al servicio
        return service.create_epic(
            name=epic_data.name, 
            description=epic_data.description,
            project_id=epic_data.project_id
        )
    except ValueError as e:
        # Si el servicio lanza un error de negocio, lo convertimos en una respuesta HTTP con código 400
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=List[EpicResponse])
def list_epics(service: EpicServiceDep):
    # El servicio devuelve Entidades de Dominio, 
    # pero FastAPI las convierte a EpicResponse automáticamente
    return service.get_all_epics()

@router.get("/{epic_id}", response_model=EpicResponse)
def get_epic(epic_id: int, service: EpicServiceDep):
    epic = service.get_epic_by_id(epic_id)
    if not epic:
        raise HTTPException(status_code=404, detail=f"Epic {epic_id} not found")
    return epic

@router.get("/project-epic/{project_id}", response_model=List[EpicResponse])
def get_epics_by_project(project_id: int, service: EpicServiceDep):
    return service.get_epics_by_project_id(project_id)

@router.put("/{epic_id}", response_model=EpicResponse)
def update_epic(epic_id: int, epic_data: EpicCreate, service: EpicServiceDep):
    try:
        # Importamos la entidad para convertir el schema de entrada
        from src.domain.entities.epic import Epic
        
        # Creamos una entidad temporal con los nuevos datos
        epic_entity = Epic(
            name=epic_data.name, 
            description=epic_data.description,
            project_id=epic_data.project_id
        )
        
        updated = service.update_epic(epic_entity, epic_id)
        if not updated:
            raise HTTPException(status_code=404, detail="Epic not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{epic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_epic(epic_id: int, service: EpicServiceDep):
    deleted = service.delete_epic(epic_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Epic not found")
    return None  # FastAPI interpretará esto como una respuesta vacía con código 204

@router.get("/count/{project_id}", response_model=int)
def count_epics_by_project(project_id: int, service: EpicServiceDep):
    return service.count_epics_by_project_id(project_id)