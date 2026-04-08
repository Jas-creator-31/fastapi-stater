from pydantic import BaseModel
from uuid import UUID


class RedisSessionValueType(BaseModel):
    user_id: UUID
    refresh_hash: str
    ip_address: str
    device_info: str
    browser: str
    os: str

class RedisSessionsSeviceReturn(BaseModel):
    access_token: str
    refresh_token: str