from src.domain.repositories.project_repository import ProjectRepository
from src.domain.entities.project import Project
from src.infrastructure.models import ProjectModel

class SQLAlchemyProjectRepository(ProjectRepository):
    def __init__(self, db: Session):
        self.db = db

    def put(self, project: Project) -> Project:
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
        project.id = db_project.id
        return project