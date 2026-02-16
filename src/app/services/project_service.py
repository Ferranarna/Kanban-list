from typing import List, Optional
from datetime import datetime
from src.domain.entities.project import Project, ProjectStatus
from src.domain.repositories.project_repository import ProjectRepository
from src.domain.repositories.epic_repository import EpicRepository

class ProjectService:
    def __init__(self, project_repository: ProjectRepository, epic_repository: EpicRepository):
        # Inyectamos la interfaz (Puerto), no la implementación
        self.project_repository = project_repository
        self.epic_repository = epic_repository

    def create_project(self, name: str, description: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, finalization_criteria: Optional[str] = None, status=ProjectStatus.ACTIVE, budget: Optional[float] = None) -> Project:
        # --- REGLA DE NEGOCIO 1: No nombres duplicados ---
        # Se busca si ya existe un proyecto con ese nombre (ignorando mayúsculas/minúsculas)
        existing_projects = self.project_repository.get_all()
        if any(p.name.lower() == name.lower() for p in existing_projects):
            raise ValueError(f"The project with name '{name}' already exists.")

        # --- REGLA DE NEGOCIO 2: Validación de longitud ---
        if len(name) < 3:
            raise ValueError("The project name must be at least 3 characters long.")

        # Creamos la entidad y la mandamos al "puerto"
        new_project = Project(name=name, description=description, start_date=start_date, end_date=end_date, finalization_criteria=finalization_criteria, status=status, budget=budget)
        return self.project_repository.add(new_project)

    def delete_project(self, project_id: int):
        # --- REGLA DE NEGOCIO 3: No borrar si tiene épicas ---
        epic_count = self.epic_repository.get_count_by_project_id(project_id)
        if epic_count > 0:
            raise ValueError(f"The project with ID {project_id} cannot be deleted because it has {epic_count} epics associated.")
        
        # --- REGLA DE NEGOCIO 4: No borrar si el estado es COMPLETED ---
        project = self.get_project_by_id(project_id)
        if project and project.status == ProjectStatus.COMPLETED:
            raise ValueError(f"The project with ID {project_id} cannot be deleted because its status is COMPLETED.")
        return self.project_repository.delete(project_id)
    
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return self.project_repository.get_by_id(project_id)
    
    def get_all_projects(self) -> List[Project]:
        return self.project_repository.get_all()
    
    def update_project(self, project_id: int, project: Project) -> Project:

        # --- REGLA DE NEGOCIO 5: Verificar que el proyecto exista ---
        existing_project = self.get_project_by_id(project_id)
        if not existing_project:
            raise ValueError(f"The project with ID {project_id} does not exist.")
        
        # --- REGLA DE NEGOCIO 6: No actualizar si el nombre ya existe (excepto para el mismo proyecto) ---
        existing_projects = self.project_repository.get_all()
        for p in existing_projects:
            if p.name.lower() == project.name.lower() and p.id != project_id:
                raise ValueError(f"The project with name '{project.name}' already exists.")
    
        # --- REGLA DE NEGOCIO 7: Validación de longitud al actualizar ---
        if len(project.name) < 3:
            raise ValueError("The project name must be at least 3 characters long.")
        
        # --- REGLA DE NEGOCIO 8: Si el proyecto está COMPLETED, no se puede cambiar su información (solo su estado) ---
        if existing_project and existing_project.status == ProjectStatus.COMPLETED:
            if project.name != existing_project.name or project.description != existing_project.description or project.end_date != existing_project.end_date or \
               project.finalization_criteria != existing_project.finalization_criteria or project.budget != existing_project.budget:
                raise ValueError(f"The project with ID {project_id} cannot be updated because its status is COMPLETED.")

        # Actualizamos el proyecto
        return self.project_repository.update(project_id, project)