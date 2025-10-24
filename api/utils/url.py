import string
import hashlib
from time import time


ALPHABET = string.digits + string.ascii_letters


def get_short_url(original_url: str, username: str) -> str:
    digest = hashlib.md5((original_url + username).encode()).hexdigest()
    md5_int = int(digest, 16) + int(time())
    return to_base62(md5_int)


def to_base62(num: int, alphabet: str = ALPHABET) -> str:
    base = len(alphabet)
    result = []
    while num > 0:
        num, rem = divmod(num, base)
        result.append(alphabet[rem])
    return "".join(reversed(result))[:6]
