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
    id: int
    name: str
    description: Optional[str] = None
    start_date: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    finalization_criteria: Optional[str] = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    budget: Optional[float] = None

    def is_overdue(self) -> bool:
        if self.end_date and self.status != ProjectStatus.COMPLETED:
            return datetime.now() > self.end_date
        return False
    
