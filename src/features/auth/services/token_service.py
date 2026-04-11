
from dotenv import load_dotenv
import os
from jwt import decode, encode
from jwt.exceptions import (
    InvalidSignatureError, 
    ExpiredSignatureError, 
    InvalidTokenError
)
from src.core.errors.domain_errors import (
    InvalidJwtSignatureError,
    InvalidJwtTokenError,
    ExpiredJwtSignatureError
)
from src.core.security.hashing_functions import hash
from src.features.auth.models import Token, TokenServiceReturn
from settings import jwt_algorithm
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from src.features.auth.types import token_type, action_type

load_dotenv()

secret = os.getenv("JWT_SECRET_KEY")
jwt_secret = str(secret)

class TokenService:
    def __init__(self) -> None:
        pass

    
    async def _create_token_payload(self, user_id, sid, type: token_type):
        now = datetime.now(timezone.utc)

        exp_time: int = 900 if type == "access" else 604800

        token_payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + timedelta(seconds=exp_time),
            "type": type,
            "sid": sid,
            "jti": str(uuid4())
        }

        return token_payload

    async def issue_token_pair(self, user_id, action: action_type, sid: UUID):

        access= await self._create_token_payload(user_id, sid, "access")
        refresh= await self._create_token_payload(user_id, sid, "refresh")
        
        access_token = encode(access, jwt_secret, jwt_algorithm)
        refresh_token = encode(refresh, jwt_secret, jwt_algorithm)

        hashed_refresh_token = await hash(refresh_token)

        return TokenServiceReturn(
            sid=sid, # type: ignore
            access_token=access_token,
            refresh_token=refresh_token,
            hashed_refresh_token=hashed_refresh_token
        )
    
    async def varify_token(self, token):
        
        try:
            decoded_token: Token = decode(token, jwt_secret, jwt_algorithm)  # type: ignore
            return decoded_token
        except ExpiredSignatureError:
            raise ExpiredJwtSignatureError
        except InvalidSignatureError:
            raise InvalidJwtSignatureError
        except InvalidTokenError:
            raise InvalidJwtTokenError

