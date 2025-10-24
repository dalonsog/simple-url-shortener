import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from api.config import Settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    data_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta    
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data_to_encode,
        Settings.SECRET_KEY,
        algorithm='HS256'
    )
    return encoded_jwt


def get_token_payload(token: str) -> dict:
    try:
        payload: dict = jwt.decode(
            token,
            Settings.SECRET_KEY,
            algorithms=['HS256']
        )
        user_email = payload.get("email")
        if not user_email:
            raise InvalidTokenError
        return {'user_email': user_email}
    except InvalidTokenError:
        raise
