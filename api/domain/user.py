from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    login: str
    email: str
    full_name: str
    password_hash: str
    created_on: datetime
    updated_on: datetime