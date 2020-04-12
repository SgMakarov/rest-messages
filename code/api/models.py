from django.db import models
from django.utils import timezone
import uuid


class Message(models.Model):
    """
    Django model for a Message. As there is no login, I decided not
    to create a model for the user and just store data in message.
    For the real project I'd created this model, reference it with
    some foreign key, but for CRUD operations on message it is
    redundant.

    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    sender_id = models.UUIDField(null=False)
    sender_name = models.TextField(
        max_length=100,
        default="sender",
    )
    receiver_id = models.UUIDField(null=False)
    receiver_name = models.TextField(
        max_length=100,
        default="receiver",
    )
    text = models.TextField(
        max_length=1024,
        editable=True,
        null=False,
    )
    date = models.DateTimeField(default=timezone.now)
