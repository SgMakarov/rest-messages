from rest_framework import serializers
from api.models import Message


class SentMessageSerializer(serializers.ModelSerializer):
    """
    A serializer class for a message. 
    Uses shorthand ModelSerializer for simplicity, contains all fields
    from the original model. Default create and update is enough for the task. 
    
    """
    class Meta:
        model = Message
        fields = ['id', 'sender_id', 'reciever_id', 'text', 'date']

class RecievedMessageSerializer(serializers.ModelSerializer):
    """
    A serializer class for a recieved message. 
    Recieved message can only be viewed, but not modified or deleted, thus
    it's id should be excluded from response. 
    
    """
    class Meta:
        model = Message
        fields = ['message_id', 'sender_name', 'reciever_id', 'reciever_name','text', 'date']
