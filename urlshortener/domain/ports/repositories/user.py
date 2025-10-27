from abc import ABC, abstractmethod
from typing import Optional

from urlshortener.domain.model.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError
    
    def add(self, user: User) -> None:
        self._add(user)

    def get_user_by_email(self, user_email: str) -> Optional[User]:
        self._get_user_by_email(user_email)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        self._get_user_by_id(user_id)

    @abstractmethod
    def _add(self, user: User) -> None:
        return NotImplementedError
    
    @abstractmethod
    def _get_user_by_email(self, user_email: str) -> Optional[User]:
        return NotImplementedError

    @abstractmethod
    def _get_user_by_id(self, user_id: str) -> Optional[User]:
        return NotImplementedError
