from dataclasses import dataclass
from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr
from urlshortener.domain.model.validators import validate_email
from bson.objectid import ObjectId


@dataclass
class User:
    id: ObjectId
    email: str
    password: str
    name: str
    created_at: datetime

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.email == other.email
    
    def __str__(self):
        return f'User("{self.email}")'
    

class RegisterUserInputDto(BaseModel):
    email: EmailStr
    password: str
    name: str


class RegisterUserOutputDto(BaseModel):
    email: EmailStr
    name: str


def user_factory(
    email: str,
    password: str,
    name: str,
    created_at: datetime = datetime.now(timezone.utc)
) -> User:
    # data validation
    for field in [email, password, name]:
        if not field:
            raise ValueError(
                'Mandatory fields "email", "password" and "name" '
                'cannot be empty'
            )
        
    if not validate_email(email):
        raise ValueError("Wrong email format")
    
    if len(name) > 20:
        raise ValueError('User name cannot be longer than 20 characters')
    
    return User(
        email=email,
        password=password,
        name=name,
        created_at=created_at
    )


def register_user_factory(
    email: str,
    password: str,
    name: str
) -> RegisterUserInputDto:
    return RegisterUserInputDto(
        email=email,
        name=name,
        password=password
    )
