from rest_framework import serializers
from .models import Message


class SentMessageSerializer(serializers.ModelSerializer):
    """
    A serializer class for a message. Uses shorthand
    ModelSerializer for simplicity, contains all fields from the
    original model. Default create and update is enough for the task.

    """

    class Meta:
        model = Message
        fields = [
            'id',
            'sender_id',
            'sender_name',
            'receiver_id',
            'receiver_name',
            'text',
            'date',
        ]


class ReceivedMessageSerializer(serializers.ModelSerializer):
    """
    A serializer class for a received message. Received message can
    only be viewed, but not modified or deleted, thus it's id
    should be excluded from response.

    """

    class Meta:
        model = Message
        fields = [
            'id',
            'sender_name',
            'receiver_id',
            'receiver_name',
            'text',
            'date'
        ]
