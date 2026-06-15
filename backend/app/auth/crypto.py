import os
from datetime import datetime, timedelta, timezone

import hashlib
import jwt
from cryptography.fernet import Fernet
from app.config import settings

_fernet = Fernet(settings.fernet.encode())

def _encrypt(plaintext: str) -> bytes:
    return _fernet.encrypt(plaintext.encode())

def _decrypt(ciphertext: bytes) -> str:
    return _fernet.decrypt(ciphertext).decode()

def _hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}:{hashed.hex()}"

def _verify_password(plain: str, hashed_password: str) -> bool:
    salt, hashed = hashed_password.split(":")
    new_hash = hashlib.pbkdf2_hmac("sha256", plain.encode(), salt.encode(), 100_000)
    return hashed == new_hash

def _create_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=72)
    }
    return jwt.encode(payload=payload, key=settings.fernet, algorithm="HS256")

def _decode_token(token: str) -> str:
    payload = jwt.decode(token, settings.fernet, algorithms=["HS256"])
    return payload["sub"]
