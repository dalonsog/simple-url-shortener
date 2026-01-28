class UserEmailAlreadyExistsException(Exception):
    def __init__(self, user_email: str) -> None:
        self.user_email = user_email


class URLKeyAlreadyExistsException(Exception):
    def __init__(self, url_key: str) -> None:
        self.url_key = url_key


class URLKeyNotFoundException(Exception):
    def __init__(self, url_key: str) -> None:
        self.url_key = url_key
