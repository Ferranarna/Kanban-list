from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(Enum):
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Task:
    epic_id: int
    name: str
    id: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    target_date: Optional[datetime] = None
    finalization_criteria: Optional[str] = None
    finalization_date: Optional[datetime] = None
    status: TaskStatus = TaskStatus.TO_DO
    assignee: Optional[str] = None
    priority: TaskPriority = TaskPriority.LOW

    def __post_init__(self):
        if not self.epic_id:
            raise ValueError("epic_id must be provided")
        if not self.name:
            raise ValueError("name must be provided")
    
    def update_info(self, name: str, description: Optional[str] = None, target_date: Optional[datetime] = None,
                     finalization_criteria: Optional[str] = None, 
                     finalization_date: Optional[datetime] = None, 
                     status: TaskStatus = TaskStatus.TO_DO, 
                     assignee: Optional[str] = None, 
                     priority: TaskPriority = TaskPriority.LOW):
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name
        self.description = description
        self.target_date = target_date
        self.finalization_criteria = finalization_criteria
        self.finalization_date = finalization_date
        self.status = status
        self.assignee = assignee
        self.priority = priority
        self.updated_at = datetime.now()
    
    def mark_as_done(self):
        self.status = TaskStatus.DONE
        self.finalization_date = datetime.now()
        self.updated_at = datetime.now()