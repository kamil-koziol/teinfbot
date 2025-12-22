from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int] = None


@dataclass
class TimeEntry:
    user_id: int

    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
