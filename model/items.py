from pydantic import BaseModel

class Item(BaseModel):
    id: int
    type: str
    key: str
    name: str
    icon: str
    status: str
    phone: int
    lost_description: str | None
    find_ip: str | None
    create_time: str
    lost_time: str | None
