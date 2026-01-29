from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.epic import Epic
from src.domain.entities.task import Task

class TaskRepository(ABC):

    @abstractmethod
    def add(self, task: Task) -> Task:
        """Create a new Task"""
        pass
    
    @abstractmethod
    def update(self, task: Task) -> Task:
        """Update an existing Task"""
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its unique ID"""
        pass

    @abstractmethod
    def get_by_epic_id(self, epic_id: int) -> List[Task]:
        """Retrieve all tasks associated with a specific epic ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        """Retrieve the list of all tasks"""
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Delete a task from the system"""
        pass

    @abstractmethod
    def get_count_by_task_id(self, task_id: int) -> int:
        """Retrieve the count of subtasks associated with a specific task ID"""
        pass
