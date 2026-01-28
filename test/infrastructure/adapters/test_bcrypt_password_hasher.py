import pytest
from urlshortener.application.ports import PasswordHasher


@pytest.mark.unit
def test_get_password_hash(bcrypt_password_hasher: PasswordHasher):
    password = 's0m3s3cr3tp4ssw0rd!'
    hashed_password = bcrypt_password_hasher.get_password_hash(password)

    assert type(hashed_password) == str


@pytest.mark.unit
def test_verify_password_successful(bcrypt_password_hasher: PasswordHasher):
    password = 's0m3s3cr3tp4ssw0rd!'
    hashed_password = bcrypt_password_hasher.get_password_hash(password)

    assert bcrypt_password_hasher.verify_password(password, hashed_password)


@pytest.mark.unit
def test_verify_wrong_password(bcrypt_password_hasher: PasswordHasher):
    password = 's0m3s3cr3tp4ssw0rd!'
    hashed_password = bcrypt_password_hasher.get_password_hash(password)

    assert not bcrypt_password_hasher.verify_password(
        'password',
        hashed_password
    )
