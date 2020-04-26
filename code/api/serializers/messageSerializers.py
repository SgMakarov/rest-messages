from rest_framework import serializers
from api.models.message import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serialize message by it's data

    I've decided to remove this thing with different views for sender and 
    reciever, as this scheme is overcomplicated and it is still unsafe, as 
    if you are able to send message to a person, you know his UUID and can 
    do everything he can. Indeed, authentification via id is very unsafe, but 
    I bellieve this is not a purpose of a task to make API as safe as possible.  

    """

    class Meta:
        model = Message
        fields = [
            'id',
            'sender_id',
            'receiver_id',
            'text',
            'date',
        ]

