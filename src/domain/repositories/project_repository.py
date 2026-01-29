from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.project import Project

class ProjectRepository(ABC):

    @abstractmethod
    def add(self, project: Project) -> Project:
        """Create a new Project"""
        pass
    
    @abstractmethod
    def update(self, project: Project) -> Project:
        """Update an existing Project"""
        pass

    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Retrieve a project by its unique ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Project]:
        """Retrieve the list of all projects"""
        pass

    @abstractmethod
    def delete(self, project_id: int) -> bool:
        """Delete a project from the system"""
        pass
