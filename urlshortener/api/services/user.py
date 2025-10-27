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
        super().__init__()
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
    
    def _get_user_by_id(self, user_id: str) -> Optional[User]:
        return self._repository.get_user_by_id(user_id)
    
    def _get_user_by_email(self, user_email: str) -> Optional[User]:
        return self._repository.get_user_by_email(user_email)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
