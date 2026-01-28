from typing import Optional
from urlshortener.domain.model.user import (
    User,
    RegisterUserInputDto,
    RegisterUserOutputDto,
    user_factory
)
from urlshortener.domain.ports.repositories.user import UserRepositoryInterface
from urlshortener.domain.ports.services.user import UserServiceInterface
from urlshortener.aplication.exception import NotAuthorizedException
from urlshortener.aplication.ports import PasswordHasher, TokenProvider


class UserService(UserServiceInterface):
    def __init__(
        self,
        password_hasher: PasswordHasher,
        token_provider: TokenProvider,
        repository: UserRepositoryInterface,
        cache: Optional[UserRepositoryInterface] = None
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._password_hasher = password_hasher
        self._token_provider = token_provider

    def create_user(
        self,
        user_dto: RegisterUserInputDto
    ) -> RegisterUserOutputDto:
        new_user = user_factory(
            email=user_dto.email,
            password=self._password_hasher.get_password_hash(user_dto.password),
            name=user_dto.name
        )
        try:
            self._repository.add(new_user)
            return new_user
        except:
            raise

    def get_user_by_email(self, user_email: str) -> Optional[User]:
        if not self._cache:
            return self._repository.get_user_by_email(user_email)
        
        user_in_cache = self._cache.get_user_by_email(user_email)
        if user_in_cache:
            return user_in_cache
        
        user_in_db = self._repository.get_user_by_email(user_email)
        if user_in_db:
            self._cache.add(user_in_db)
        
        return user_in_db
    
    def login_user(
        self,
        user_email: str,
        user_pwd: str,
        secret_key: str
    ) -> str:
        user: User = self.get_user_by_email(user_email)
        if (
            not user or
            not self._password_hasher.verify_password(user_pwd, user.password)
        ):
            raise NotAuthorizedException()
        
        return self._token_provider.create_access_token(
            {'email': user_email},
            secret_key
        )
