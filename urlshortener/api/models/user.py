from mongoengine import StringField, DateTimeField, EmailField
from api.models import db
from datetime import datetime, timezone


class User(db.Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(max_length=20, required=True)
    created_at = DateTimeField(default=datetime.now(timezone.utc), null=False)
