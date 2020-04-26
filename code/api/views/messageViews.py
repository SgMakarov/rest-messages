from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins

from api.models.user import User
from api.serializers.userSerializers import UserSerializer
from api.models.message import Message
from api.serializers.messageSerializers import MessageSerializer

@method_decorator(name="create", decorator=swagger_auto_schema(
    operation_summary="Create new message by text, UUID of sender and receiver",
    responses={
        400: "Bad request: bad format of UUID or some field is missed",
        201: "User is created",
    }
))
class MessageViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    ):
    
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
