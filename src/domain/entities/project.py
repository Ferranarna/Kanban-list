from dataclasses import dataclass, field
from datetime import datetimefrom typing import Optional
from enum import enum

class ProjectStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

@dataclass
class Project:
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    start_date: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    finalization_criteria: Optional[str] = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    budget: Optional[float] = None

    def __post_init__(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date")
    
    def update_info (self, name: str, description: Optional[str] = None, end_date: Optional[datetime] = None, 
                     finalization_criteria: Optional[str] = None, 
                     status: ProjectStatus = ProjectStatus.ACTIVE, 
                     budget: Optional[float] = None):
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name
        self.description = description
        self.end_date = end_date
        self.finalization_criteria = finalization_criteria
        self.status = status
        self.budget = budget
        self.updated_at = datetime.now()

    

    
