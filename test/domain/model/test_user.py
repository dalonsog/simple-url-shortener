import pytest
from datetime import datetime
from pydantic import ValidationError
from urlshortener.domain.model.user import (
    User,
    RegisterUserInputDto,
    user_factory,
    register_user_factory
)


@pytest.mark.unit
def test_create_user_valid_parameters():
    user = User(
        email='user@domain.com',
        password='s0m3s3cr3tp4ssw0rd!',
        name='User',
        created_at=datetime.now()
    )
    assert isinstance(user, User)


@pytest.mark.unit
def test_create_user_missing_parameter():
    with pytest.raises(TypeError):
        User(
            email='user@domain.com',
            password='s0m3s3cr3tp4ssw0rd!',
            name='User'
        )


@pytest.mark.unit
def test_compare_two_equal_users():
    user1 = User(
        email='user@domain.com',
        password='s0m3s3cr3tp4ssw0rd!',
        name='User',
        created_at=datetime.now()
    )

    user2 = User(
        email='user@domain.com',
        password='s0m3s3cr3tp4ssw0rd!',
        name='User',
        created_at=datetime.now()
    )

    assert user1 == user2


@pytest.mark.unit
def test_compare_two_different_users():
    user1 = User(
        email='user@domain.com',
        password='s0m3s3cr3tp4ssw0rd!',
        name='User',
        created_at=datetime.now()
    )

    user2 = User(
        email='user2@domain.com',
        password='s0m3s3cr3tp4ssw0rd!',
        name='User',
        created_at=datetime.now()
    )

    assert user1 != user2
    

@pytest.mark.unit
def test_string_representation():
    user = User(
        email='user@domain.com',
        password='s0m3s3cr3tp4ssw0rd!',
        name='User',
        created_at=datetime.now()
    )

    assert str(user) == 'User("user@domain.com")'


@pytest.mark.unit
def test_create_user_with_factory_function():
    email = 'user@domain.com'
    password = 's0m3s3cr3tp4ssw0rd!'
    name = 'User'
    created_at = datetime.now()
    user = user_factory(
        email=email,
        password=password,
        name=name,
        created_at=created_at
    )
    
    assert isinstance(user, User)
    assert user.email == email
    assert user.password == password
    assert user.name == name
    assert user.created_at == created_at


@pytest.mark.unit
def test_create_user_with_factory_function_missing_creation_time():
    email = 'user@domain.com'
    password = 's0m3s3cr3tp4ssw0rd!'
    name = 'User'
    user = user_factory(
        email=email,
        password=password,
        name=name
    )
    
    assert isinstance(user, User)
    assert user.email == email
    assert user.password == password
    assert user.name == name
    assert isinstance(user.created_at, datetime)


@pytest.mark.unit
def test_create_user_with_factory_function_wrong_email():
    with pytest.raises(ValueError):
        user_factory(
            email='wrong.emailATdomain.com',
            password='s0m3s3cr3tp4ssw0rd!',
            name='User'
        )


@pytest.mark.unit
def test_create_user_with_factory_function_long_name():
    with pytest.raises(ValueError):
        user_factory(
            email='wrong.emailATdomain.com',
            password='s0m3s3cr3tp4ssw0rd!',
            name='Some extremely long user name'
        )


@pytest.mark.unit
def test_create_register_user_dto():
    data = {
        'email': 'user@domain.com',
        'password': 's0m3s3cr3tp4ssw0rd!',
        'name': 'User'
    }

    register_user = RegisterUserInputDto(**data)
    assert isinstance(register_user, RegisterUserInputDto)


@pytest.mark.unit
def test_create_register_user_dto_wrong_email_format():
    data = {
        'email': 'userATdomain.com',
        'password': 's0m3s3cr3tp4ssw0rd!',
        'name': 'User'
    }

    with pytest.raises(ValidationError):
        RegisterUserInputDto(**data)


@pytest.mark.unit
def test_create_register_user_with_factory():
    email = 'user@domain.com'
    password = 's0m3s3cr3tp4ssw0rd!'
    name = 'User'

    register_user = register_user_factory(
        email=email,
        password=password,
        name=name
    )

    assert isinstance(register_user, RegisterUserInputDto)
    assert register_user.email == email
    assert register_user.password == password
    assert register_user.name == name
