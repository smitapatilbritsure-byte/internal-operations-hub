from typing import Any, Dict
# pyrefly: ignore [missing-import]
from jose import jwt, JWTError
# pyrefly: ignore [missing-import]
from core.config import settings

def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
