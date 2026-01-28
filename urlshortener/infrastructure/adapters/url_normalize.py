from url_normalize import url_normalize
from urlshortener.application.ports import UrlNormalizer


class UrlNormalize(UrlNormalizer):
    def normalize_url(self, url: str) -> str:
        return url_normalize(url)
