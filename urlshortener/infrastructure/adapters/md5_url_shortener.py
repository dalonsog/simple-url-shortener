import string
import hashlib
from random import randint
from urlshortener.application.ports import UrlShortener


class MD5UrlShortener(UrlShortener):
    _ALPHABET = string.digits + string.ascii_letters

    def get_short_url(self, url: str, user: str) -> str:
        digest = hashlib.md5((
            url + user + str(randint(10000, 50000))
        ).encode()).hexdigest()
        md5_int = int(digest, 16)
        return self._to_base62(md5_int)
    
    def _to_base62(self, num: int) -> str:
        base = len(MD5UrlShortener._ALPHABET)
        result = []
        while num > 0:
            num, rem = divmod(num, base)
            result.append(MD5UrlShortener._ALPHABET[rem])
        return "".join(reversed(result))[:6]
