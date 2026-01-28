from abc import abstractmethod, ABC


class PasswordHasher(ABC):
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        raise NotImplementedError
