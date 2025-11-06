from typing import Optional
from urlshortener.infrastructure.db.models.user import UserDB
from urlshortener.domain.model.user import User, user_factory
from urlshortener.domain.ports.repositories.user import UserRepositoryInterface
from urlshortener.domain.ports.repositories.exceptions import (
    UserDBOperationError
)


class UserRepository(UserRepositoryInterface):
    def __init__(self) -> None:
        pass
    
    def _add(self, user: User) -> None:
        user_in_db = self.get_user_by_email(user_email=user.email)
        if user_in_db:
            raise UserDBOperationError(f'User {user.email} already exists')
        
        try:
            user_db = UserDB(
                email=user.email,
                password=user.password,
                name=user.name,
                created_at=user.created_at
            )
            user_db.save()
        except Exception as excpt:
            raise UserDBOperationError(excpt)
    
    def _get_user_by_email(self, user_email: str) -> Optional[User]:
        user_db: UserDB = UserDB.objects(email=user_email).first()
        if user_db:
            return user_factory(
                email=user_db.email,
                password=user_db.password,
                name=user_db.name,
                created_at=user_db.created_at
            )
        else:
            return None
