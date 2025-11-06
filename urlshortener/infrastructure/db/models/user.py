from mongoengine import StringField, DateTimeField, EmailField
from datetime import datetime, timezone
from urlshortener.infrastructure.db import db


class UserDB(db.Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(max_length=20, required=True)
    created_at = DateTimeField(default=datetime.now(timezone.utc), null=False)
