import secrets
import httpx
import uuid
from jwt import ExpiredSignatureError, InvalidTokenError

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.config import settings
from app.api.models import UserAlpacaToken, Users
from app.api.database import get_db
from app.auth.crypto import (
    _encrypt,
    _hash_password,
    _verify_password,
    _create_token,
    _decode_token,
)
from app.auth.schemas import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> uuid.UUID:
    try:
        return uuid.UUID(_decode_token(token=token))
    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except InvalidTokenError:
        raise HTTPException(401, "Invalid token")


@router.post("/register")
async def register(body: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(Users).filter(Users.email == body.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")

    user = Users(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        hashed_password=_hash_password(password=body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user_id": user.id}


@router.post("/login")
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == body.email).first()
    if not user or not _verify_password(
        plain=body.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": _create_token(user_id=str(user.id))}


@router.get("/alpaca/connect")
async def alpaca_connect(
    request: Request, user_id: uuid.UUID = Depends(get_current_user)
):
    random = secrets.token_urlsafe(32)
    state = f"{random}:{user_id}"
    callback_url = str(request.base_url) + "auth/alpaca/callback"
    request.session["oauth_state"] = state
    url = (
        "https://app.alpaca.markets/oauth/authorize"
        f"?response_type=code"
        f"&client_id={settings.alpaca_app_client_id}"
        f"&redirect_uri={callback_url}"
        f"&state={state}"
        f"&scope=account:write%20trading"
        f"&env=paper"
    )
    return RedirectResponse(url=url)


@router.get("/alpaca/callback")
async def alpaca_callback(
    request: Request,
    code: str,
    state: str,
    user_id: uuid.UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stored_state = request.session.pop("oauth_state", None)

    if not stored_state or state != stored_state:
        raise HTTPException(400, "Invalid state")

    callback_url = str(request.base_url) + "auth/alpaca/callback"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://api.alpaca.markets/oauth/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.alpaca_app_client_id,
                "client_secret": settings.alpaca_app_client_secret,
                "redirect_uri": callback_url,
            },
            headers={
                "accept": "application/json",
                "content-type": "application/x-www-form-urlencoded",
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    tokens = response.json()

    existing_alpaca_token = (
        db.query(UserAlpacaToken).filter(UserAlpacaToken.user_id == user_id).first()
    )
    if existing_alpaca_token:
        existing_alpaca_token.access_token_enc = _encrypt(tokens["access_token"])
        existing_alpaca_token.token_type = tokens["token_type"]
        existing_alpaca_token.scope = tokens["scope"]
        existing_alpaca_token.is_active = True
        existing_alpaca_token.revoked_at = None
    else:
        alpaca_token = UserAlpacaToken(
            access_token_enc=_encrypt(tokens["access_token"]),
            user_id=user_id,
            token_type=tokens["token_type"],
            scope=tokens["scope"],
        )
        db.add(alpaca_token)

    db.commit()
