from typing import List, Optional
from src.domain.entities.epic import Epic, EpicStatus
from src.domain.repositories.project_repository import ProjectRepository
from src.domain.repositories.epic_repository import EpicRepository

class EpicService:
    def __init__(self, epic_repository: EpicRepository, project_repository: ProjectRepository):
        # Inyectamos la interfaz (Puerto), no la implementación
        self.epic_repository = epic_repository
        self.project_repository = project_repository

    def create_epic(self, name: str, project_id: int, description: Optional[str] = None) -> Epic:
        # --- REGLA DE NEGOCIO 1: Verificar que el proyecto exista ---
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"The project with ID {project_id} does not exist.")

        # --- REGLA DE NEGOCIO 2: No nombres duplicados dentro del mismo proyecto ---
        existing_epics = self.epic_repository.get_by_project_id(project_id)
        if any(e.name.lower() == name.lower() for e in existing_epics):
            raise ValueError(f"The epic with name '{name}' already exists in project ID {project_id}.")

        # Creamos la entidad y la mandamos al "puerto"
        new_epic = Epic(name=name, project_id=project_id, description=description)
        return self.epic_repository.add(new_epic)
    
    def get_epic_by_id(self, epic_id: int) -> Optional[Epic]:
        return self.epic_repository.get_by_id(epic_id)
    
    def get_all_epics(self) -> List[Epic]:
        return self.epic_repository.get_all()
    
    def update_epic(self, epic: Epic, epic_id: int) -> Epic:
        
        # --- REGLA DE NEGOCIO 3: Verificar que la épica exista ---
        existing_epic = self.get_epic_by_id(epic_id)
        if not existing_epic:
            raise ValueError(f"The epic with ID {epic_id} does not exist.")
        
        # --- REGLA DE NEGOCIO 4: No actualizar si el nombre ya existe (excepto para la misma épica) ---
        existing_epics = self.epic_repository.get_by_project_id(existing_epic.project_id)
        for e in existing_epics:
            if e.name.lower() == epic.name.lower() and e.id != epic_id:
                raise ValueError(f"The epic with name '{epic.name}' already exists in project ID {existing_epic.project_id}.")
        
        # --- REGLA DE NEGOCIO 5: No actualizar si la épica está COMPLETED, solo el estado ---
        if existing_epic.status == EpicStatus.COMPLETED:
            if epic.name != existing_epic.name or epic.description != existing_epic.description or epic.start_date != existing_epic.start_date or \
               epic.end_date != existing_epic.end_date or epic.project_id != existing_epic.project_id:
                raise ValueError(f"The epic with ID {epic_id} cannot be updated because its status is COMPLETED.")

        # Actualizamos la épica
        epic.id = epic_id
        return self.epic_repository.update(epic)
    
    def delete_epic(self, epic_id: int):
        # --- REGLA DE NEGOCIO 6: Verificar que la épica exista antes de eliminar ---
        existing_epic = self.get_epic_by_id(epic_id)
        if not existing_epic:
            raise ValueError(f"The epic with ID {epic_id} does not exist.")
        
        # --- REGLA DE NEGOCIO 7: No borrar si la épica está COMPLETED ---
        if existing_epic.status == EpicStatus.COMPLETED:
            raise ValueError(f"The epic with ID {epic_id} cannot be deleted because its status is COMPLETED.")
        
        return self.epic_repository.delete(epic_id)
    
    def get_epics_by_project_id(self, project_id: int) -> List[Epic]:
        #  --- REGLA DE NEGOCIO 8: Verificar que el proyecto exista ---
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"The project with ID {project_id} does not exist.")
        
        return self.epic_repository.get_by_project_id(project_id)
    
