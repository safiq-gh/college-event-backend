from pydantic import BaseModel, EmailStr
from typing import List

class RegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    college: str
    department: str
    year: int
    event_ids: List[str]
    transaction_id: str