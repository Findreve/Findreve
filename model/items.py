from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: int
    type: str
    key: str
    name: str
    icon: str
    status: str
    phone: int
    lost_description: Optional[str]
    find_ip: Optional[str]
    create_time: str
    lost_time: Optional[str]
    