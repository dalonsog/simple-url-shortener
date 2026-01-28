from passlib.context import CryptContext
from urlshortener.aplication.ports import PasswordHasher


class BCryptPasswordHasher(PasswordHasher):
    _PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> str:
        return BCryptPasswordHasher._PWD_CONTEXT.verify(
            plain_password,
            hashed_password
        )
    
    def get_password_hash(self, password: str) -> str:
        return BCryptPasswordHasher._PWD_CONTEXT.hash(password)
