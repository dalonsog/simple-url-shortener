from typing import Optional
from urlshortener.domain.model.user import User
from urlshortener.domain.ports.repositories.user import UserRepositoryInterface
from urlshortener.domain.ports.repositories.exceptions import (
    UserDBOperationError
)


class FakeUserRepository(UserRepositoryInterface):
    def __init__(self) -> None:
        self._database: dict[str, User] = {}
    
    def _add(self, user: User) -> None:
        user_in_db = self.get_user_by_email(user.email)
        if user_in_db:
            raise UserDBOperationError(f'User {user.email} already exists')
        
        self._database[user.email] 
    
    def _get_user_by_email(self, user_email: str) -> Optional[User]:
        return self._database[user_email]
