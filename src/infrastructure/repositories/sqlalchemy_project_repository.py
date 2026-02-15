import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.repositories.project_repository import ProjectRepository
from src.domain.entities.project import Project, ProjectStatus
from src.infrastructure.models import ProjectModel

class SQLAlchemyProjectRepository(ProjectRepository):
    def __init__(self, db: Session):
        self.db = db
    
    # funcion privada para convertir de modelo de DB a entidad de Dominio y evitar repetición de código y errores de Pylance
    def _to_entity(self, db_model: ProjectModel) -> Project:
        return Project(
            # Usamos variables intermedias si Pylance sigue quejándose
            # o simplemente nos aseguramos de que no sean nulos donde no deben
            id=int(db_model.id) if db_model.id is not None else None, # type: ignore
            name=str(db_model.name), # type: ignore
            description=str(db_model.description) if db_model.description else None, # type: ignore
            finalization_criteria=str(db_model.finalization_criteria) if db_model.finalization_criteria else None, # type: ignore
            status=ProjectStatus(db_model.status) if db_model.status else None, # type: ignore
            budget=float(db_model.budget) if db_model.budget is not None else None, # type: ignore
            start_date=db_model.start_date if db_model.start_date else datetime.datetime.now(), # type: ignore
            updated_at=datetime.datetime.now() if db_model.updated_at is None else db_model.updated_at, # type: ignore
            end_date=db_model.end_date if db_model.end_date else None # type: ignore
        )

    def add(self, project: Project) -> Project:
        # 1. Convertimos la Entidad de Dominio en un Modelo de DB
        db_project = ProjectModel(
            name=project.name,
            description=project.description,
            finalization_criteria=project.finalization_criteria,
            status=project.status,
            budget=project.budget,
            end_date=project.end_date
        )
        # 2. Guardamos en MySQL
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project) # Para obtener el ID generado automáticamente
        
        # 3. Devolvemos el objeto actualizado con su ID
        project.id = db_project.id if isinstance(db_project.id, int) else None
        return self._to_entity(db_project)
    
    def update(self, project_id:int, project: Project) -> Optional[Project]:
        db_project = self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        if not db_project:
            raise ValueError("Project not found")
        
        #Actualizamos los campos en los que se ha escrito alguna información
        #Usamos ignore para evitar errores marcados por Pylance por la duda de tipos en el metacodigo de sqlalchemy
        
        if project.name is not None:
            db_project.name = project.name # type: ignore
            
        if project.description is not None:
            db_project.description = project.description # type: ignore
            
        if project.finalization_criteria is not None:
            db_project.finalization_criteria = project.finalization_criteria # type: ignore
            
        if project.status is not None:
            db_project.status = project.status # type: ignore
            
        if project.budget is not None:
            db_project.budget = project.budget # type: ignore
            
        if project.end_date is not None:
            db_project.end_date = project.end_date  # type: ignore
        
        db_project.updated_at = datetime.datetime.now()  # type: ignore
        
        self.db.commit()
        self.db.refresh(db_project)
        
        return self._to_entity(db_project)
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        db_project = self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        if not db_project:
            raise ValueError("Project not found")
        
        return self._to_entity(db_project)
    
    def get_all(self) -> Optional[List[Project]]:
        db_projects = self.db.query(ProjectModel).all()
        if len(db_projects) != 0:
            if not db_projects:
                raise ValueError("No projects found")
        
        #Retornamos una lista de db_project como hemos tipado en la función
        return [self._to_entity(db_project) for db_project in db_projects]
    
    def delete(self, project_id: int) -> bool:
        db_project = self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        if not db_project:
            raise ValueError("Project not found")
        
        self.db.delete(db_project)
        self.db.commit()
        return True