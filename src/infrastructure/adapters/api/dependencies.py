from typing import Annotated, Generator
from fastapi.params import Depends
from sqlalchemy.orm import Session
from src.infrastructure.database import SessionLocal
from src.infrastructure.repositories.sqlalchemy_project_repository import SQLAlchemyProjectRepository
from src.infrastructure.repositories.sqlalchemy_epic_repository import SQLAlchemyEpicRepository
from src.infrastructure.repositories.sqlalchemy_task_repository import SQLAlchemyTaskRepository
from src.app.services.project_service import ProjectService
from src.app.services.epic_service import EpicService
from src.app.services.task_service import TaskService


# 1. Proveedor de la sesión de base de datos
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Definimos un "Alias" para no repetir código
# Esto dice: "Es una Session, pero se obtiene vía Depends(get_db)"
DbSession = Annotated[Session, Depends(get_db)]
#El Tipo (Session): Esto es para el editor (Pylance). Le dice: "Lo que hay aquí dentro se comporta como una sesión de base de datos".
#El Metadato (Depends(get_db)): Esto es una nota adhesiva que solo lee FastAPI. Le dice: "Cuando alguien pida esta caja, primero ejecuta la función get_db y mete el resultado dentro".

# 2. Proveedor del Servicio de Proyectos
def get_project_service(db: DbSession) -> ProjectService:
    # Aquí es donde ocurre el "ensamblaje"
    repo = SQLAlchemyProjectRepository(db)
    epic_repo = SQLAlchemyEpicRepository(db) # Lo necesita para validar reglas de negocio
    return ProjectService(repo, epic_repo)

# 3. Proveedor del Servicio de Épicas
def get_epic_service(db: DbSession) -> EpicService:
    repo = SQLAlchemyEpicRepository(db)
    project_repo = SQLAlchemyProjectRepository(db)
    return EpicService(repo, project_repo)

# 4. Proveedor del Servicio de Tareas
def get_task_service(db: DbSession) -> TaskService:
    repo = SQLAlchemyTaskRepository(db)
    epic_repo = SQLAlchemyEpicRepository(db)
    return TaskService(repo, epic_repo)