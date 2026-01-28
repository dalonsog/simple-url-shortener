from abc import abstractmethod, ABC
from datetime import timedelta


class TokenProvider(ABC):
    @abstractmethod
    def create_access_token(
        self,
        data: dict,
        secret_key: str,
        expires_delta: timedelta
    ) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_token_payload(self, token: str, secret_key: str,) -> dict:
        raise NotImplementedError
