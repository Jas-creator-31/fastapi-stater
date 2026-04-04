from typing import TypedDict
from uuid import UUID

class RedisSessionValueType(TypedDict):
    user_id: UUID
    refresh_hash: str
    ip_address: str
    device_info: str
    browser: str
    os: str