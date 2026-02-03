from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class EpicStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class EpicPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Epic:
    project_id: int
    name: str
    id: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    completion_criteria: Optional[str] = None
    status: EpicStatus = EpicStatus.NOT_STARTED
    priority: EpicPriority = EpicPriority.LOW

    def __post_init__(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date")
        if not self.project_id:
            raise ValueError("project_id must be provided")
    
    def update_info(self, name: str, description: Optional[str] = None, start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None, 
                     completion_criteria: Optional[str] = None, 
                     status: EpicStatus = EpicStatus.NOT_STARTED, 
                     priority: EpicPriority = EpicPriority.LOW):
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.completion_criteria = completion_criteria
        self.status = status
        self.priority = priority
        self.updated_at = datetime.now()

    