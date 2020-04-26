from django.db import models
from django.utils import timezone
from api.models.user import User
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
    sender_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name="sent_messages",
    )
    receiver_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name="received_messages",
    )
    text = models.TextField(
        max_length=1024,
        editable=True,
        null=False,
    )
    date = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
