from datetime import datetime, timezone
from mongoengine import StringField, DateTimeField, IntField, ReferenceField
from urlshortener.infrastructure.db import db
from urlshortener.infrastructure.models.user import UserDB


class URLDB(db.Document):
    short_url = StringField(max_length=6, primary_key=True)
    original_url = StringField(max_length=200, null=False, required=True)
    clicks = IntField(default=0)
    user = ReferenceField(UserDB, required=True)
    created_at = DateTimeField(default=datetime.now(timezone.utc), null=False)
