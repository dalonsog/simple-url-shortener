from abc import abstractmethod, ABC


class UrlShortener(ABC):
    @abstractmethod
    def get_short_url(self, url: str, user: str) -> str:
        raise NotImplementedError
