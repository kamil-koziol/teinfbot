from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int


@dataclass
class TimeEntry:
    id: int
    user_id: int
    created_at: datetime
