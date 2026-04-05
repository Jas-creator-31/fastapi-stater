from src.features.auth.create_jwt_payload import create_jwt_payload
from dotenv import load_dotenv
import os
import jwt
from src.core.security.hashing_functions import hash
from src.features.auth.models import TokenServiceReturn

load_dotenv()

secret = os.getenv("JWT_SECRET_KEY")
jwt_secret = str(secret)

class TokenService:
    def __init__(self) -> None:
        pass

    async def issue_jwt(self, user_id):

        access, refresh = await create_jwt_payload(user_id)

        sid = access["sid"] # both tokens share one sid 
        
        access_token = jwt.encode(access, access["sid"], jwt_secret)
        refresh_token = jwt.encode(refresh, refresh["sid"], jwt_secret)

        hashed_refresh_token = await hash(refresh_token)

        return TokenServiceReturn(
            sid=sid,
            access_token=access_token,
            refresh_token=refresh_token,
            hashed_refresh_token=hashed_refresh_token
        )