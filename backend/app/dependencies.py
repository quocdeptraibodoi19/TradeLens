import uuid

from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, InvalidTokenError

from sqlalchemy.orm import Session

from app.api.models import UserAlpacaToken
from app.api.database import get_db
from app.api.services.auth.crypto import _decrypt, _decode_token

http_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> uuid.UUID:
    token = request.cookies.get("access_token")
    if not token and credentials:
        token = credentials.credentials
    if not token:
        raise HTTPException(401, "Not authenticated")
    try:
        return uuid.UUID(_decode_token(token=token))
    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except InvalidTokenError:
        raise HTTPException(401, "Invalid token")


def get_alpaca_access_token(
    user_id: uuid.UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> str:
    token = (
        db.query(UserAlpacaToken)
        .filter(UserAlpacaToken.user_id == user_id, UserAlpacaToken.is_active == True)
        .first()
    )
    if not token:
        raise HTTPException(404, "Alpaca account not connected")
    return _decrypt(token.access_token_enc)
