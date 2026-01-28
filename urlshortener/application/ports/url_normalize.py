from abc import abstractmethod, ABC


class UrlNormalizer(ABC):
    @abstractmethod
    def normalize_url(self, url: str) -> str:
        raise NotImplementedError
