from abc import ABC, abstractmethod
from typing import Optional

from urlshortener.domain.model.user import (
    User,
    RegisterUserInputDto,
    RegisterUserOutputDto
)


class UserServiceInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError
    
    def create(self, user: RegisterUserInputDto) -> RegisterUserOutputDto:
        return self._create(user)
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self._get_user_by_uid(user_id)
    
    def get_user_by_email(self, user_email: str) -> Optional[User]:
        return self._get_user_by_email(user_email)
    
    @abstractmethod
    def _create(self, user: RegisterUserInputDto) -> RegisterUserOutputDto:
        raise NotImplementedError
    
    @abstractmethod
    def _get_user_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError
    
    @abstractmethod
    def _get_user_by_email(self, user_email: str) -> Optional[User]:
        raise NotImplementedError
