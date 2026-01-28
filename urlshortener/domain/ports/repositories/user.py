from abc import ABC, abstractmethod
from typing import Optional

from urlshortener.domain.model.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        return NotImplementedError

    @abstractmethod
    def get_user_by_email(self, user_email: str) -> Optional[User]:
        return NotImplementedError
