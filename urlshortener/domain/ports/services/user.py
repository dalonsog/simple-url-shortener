from abc import ABC, abstractmethod
from typing import Optional
from urlshortener.domain.model.user import (
    User,
    RegisterUserInputDto,
    RegisterUserOutputDto
)


class UserServiceInterface(ABC):
    @abstractmethod
    def create_user(
        self,
        user_dto: RegisterUserInputDto
    ) -> RegisterUserOutputDto:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, user_email: str) -> Optional[User]:
        raise NotImplementedError
    
    @abstractmethod
    def login_user(
        self,
        user_email: str,
        user_pwd: str,
        secret_key: str
    ) -> str:
        raise NotImplementedError
