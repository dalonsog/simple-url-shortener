import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from urlshortener.domain.ports.services.user import UserServiceInterface
from urlshortener.domain.model.user import (
    User,
    RegisterUserInputDto,
    RegisterUserOutputDto,
    user_factory
)
from urlshortener.domain.ports.repositories.user import UserRepositoryInterface


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(UserServiceInterface):
    def __init__(self, repository: UserRepositoryInterface) -> None:
        self._repository = repository
    
    def _create(self, user: RegisterUserInputDto) -> RegisterUserOutputDto:
        new_user = user_factory(
            email=user.email,
            password=UserService.get_password_hash(user.password),
            name=user.name
        )
        try:
            self._repository.add(new_user)
            return new_user
        except:
            raise
    
    def _get_user_by_email(self, user_email: str) -> Optional[User]:
        return self._repository.get_user_by_email(user_email)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(
        data: dict,
        secret_key: str,
        expires_delta: timedelta = timedelta(minutes=150)
    ) -> str:
        data_to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta    
        data_to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            data_to_encode,
            secret_key,
            algorithm='HS256'
        )
        return encoded_jwt

    @staticmethod
    def get_token_payload(token: str, secret_key: str,) -> dict:
        try:
            payload: dict = jwt.decode(
                token,
                secret_key,
                algorithms=['HS256']
            )
            user_email = payload.get("email")
            if not user_email:
                raise InvalidTokenError
            return {'user_email': user_email}
        except InvalidTokenError:
            raise
