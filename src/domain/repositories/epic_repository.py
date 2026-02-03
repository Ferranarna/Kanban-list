from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.epic import Epic

class EpicRepository(ABC):

    @abstractmethod
    def add(self, epic: Epic) -> Epic:
        """Create a new Epic"""
        pass
    
    @abstractmethod
    def update(self, epic: Epic) -> Epic:
        """Update an existing Epic"""
        pass

    @abstractmethod
    def get_by_id(self, epic_id: int) -> Optional[Epic]:
        """Retrieve an epic by its unique ID"""
        pass

    @abstractmethod
    def get_by_project_id(self, project_id: int) -> List[Epic]:
        """Retrieve all epics associated with a specific project ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Epic]:
        """Retrieve the list of all epics"""
        pass

    @abstractmethod
    def delete(self, epic_id: int) -> bool:
        """Delete an epic from the system"""
        pass
    
    @abstractmethod
    def get_count_by_project_id(self, project_id: int) -> int:
        """Get the count of epics associated with a specific project ID"""
        pass