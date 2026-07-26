from dataclasses import dataclass
from datetime import datetime


@dataclass
class FollowingAccount:
    username: str
    date_followed: datetime
    notes: str = ""
    status: str = "undecided"
    category: str | None = None