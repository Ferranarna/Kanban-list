import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.repositories.epic_repository import EpicRepository
from src.domain.entities.epic import Epic, EpicPriority, EpicStatus
from src.infrastructure.models import EpicModel

class SQLAlchemyEpicRepository(EpicRepository):
    def __init__(self, db: Session):
        self.db = db
    
    # funcion privada para convertir de modelo de DB a entidad de Dominio y evitar repetición de código y errores de Pylance
    def _to_entity(self, db_model: EpicModel) -> Epic:
        return Epic(
            # Usamos variables intermedias si Pylance sigue quejándose
            # o simplemente nos aseguramos de que no sean nulos donde no deben
            project_id=int(db_model.project_id), # type: ignore
            name=str(db_model.name), # type: ignore
            id=int(db_model.id) if db_model.id is not None else None, # type: ignore
            description=str(db_model.description) if db_model.description else None, # type: ignore
            completion_criteria=str(db_model.completion_criteria) if db_model.completion_criteria else None, # type: ignore
            status=EpicStatus(db_model.status) if db_model.status else None, # type: ignore
            priority=EpicPriority(db_model.priority) if db_model.priority else None, # type: ignore
            start_date=db_model.start_date if db_model.start_date else datetime.datetime.now(), # type: ignore
            updated_at=datetime.datetime.now() if db_model.updated_at is None else db_model.updated_at, # type: ignore
            end_date=db_model.end_date if db_model.end_date else None # type: ignore
        )

    def add(self, epic: Epic) -> Epic:
        # 1. Convertimos la Entidad de Dominio en un Modelo de DB
        db_epic = EpicModel(
            project_id=epic.project_id,
            name=epic.name,
            description=epic.description,
            completion_criteria=epic.completion_criteria,
            status=epic.status.value,
            priority=epic.priority.value,
            start_date=epic.start_date,
            end_date=epic.end_date
        )
        # 2. Guardamos en MySQL
        self.db.add(db_epic)
        self.db.commit()
        self.db.refresh(db_epic) # Para obtener el ID generado automáticamente
        
        # 3. Devolvemos el objeto actualizado con su ID
        epic.id = db_epic.id if isinstance(db_epic.id, int) else None
        return self._to_entity(db_epic)
    
    def update(self, epic_id:int, epic: Epic) -> Optional[Epic]:
        db_epic = self.db.query(EpicModel).filter(EpicModel.id == epic_id).first()
        if not db_epic:
            raise ValueError("Epic not found")
        
        #Actualizamos los campos en los que se ha escrito alguna información
        #Usamos ignore para evitar errores marcados por Pylance por la duda de tipos en el metacodigo de sqlalchemy
        
        if epic.name is not None:
            db_epic.name = epic.name # type: ignore
            
        if epic.description is not None:
            db_epic.description = epic.description # type: ignore
            
        if epic.completion_criteria is not None:
            db_epic.completion_criteria = epic.completion_criteria # type: ignore
            
        if epic.status is not None:
            db_epic.status = epic.status.value # type: ignore

        if epic.priority is not None:
            db_epic.priority = epic.priority.value  # type: ignore
            
        if epic.end_date is not None:
            db_epic.end_date = epic.end_date  # type: ignore
        
        db_epic.updated_at = datetime.datetime.now()  # type: ignore
        
        self.db.commit()
        self.db.refresh(db_epic)
        
        return self._to_entity(db_epic)
    
    def get_by_id(self, epic_id: int) -> Optional[Epic]:
        db_epic = self.db.query(EpicModel).filter(EpicModel.id == epic_id).first()
        if not db_epic:
            raise ValueError("Epic not found")
        
        return self._to_entity(db_epic)
    
    def get_all(self) -> Optional[List[Epic]]:
        db_epics = self.db.query(EpicModel).all()
        if not db_epics:
            raise ValueError("No epics found")
        
        #Retornamos una lista de db_epic como hemos tipado en la función
        return [self._to_entity(db_epic) for db_epic in db_epics]
    
    def get_by_project_id(self, project_id: int) -> Optional[List[Epic]]:
        db_epics = self.db.query(EpicModel).filter(EpicModel.project_id == project_id).all()
        if not project_id:
            raise ValueError("Project ID must be provided")
        if not db_epics:
            raise ValueError("No epics found for the given project ID")
        return [self._to_entity(db_epic) for db_epic in db_epics]
    
    def delete(self, epic_id: int) -> bool:
        db_epic = self.db.query(EpicModel).filter(EpicModel.id == epic_id).first()
        if not db_epic:
            raise ValueError("Epic not found")
        
        self.db.delete(db_epic)
        self.db.commit()
        return True
    
    def get_count_by_project_id(self, project_id: int) -> int:
        count = self.db.query(EpicModel).filter(EpicModel.project_id == project_id).count()
        return count