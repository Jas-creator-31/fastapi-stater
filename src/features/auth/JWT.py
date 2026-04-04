from uuid import uuid4
from datetime import datetime, timezone, timedelta

async def create_jwt_payload(user_id):
    now = datetime.now(timezone.utc)

    sid = uuid4()
    access_payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=15),
        "type": "access",
        "sid": sid,
        "jti": str(uuid4())
    }

    refresh_payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(days=7),
        "type": "refresh",
        "sid": sid,
        "jti": str(uuid4())
    }

    return access_payload, refresh_payload