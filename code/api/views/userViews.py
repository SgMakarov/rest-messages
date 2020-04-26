from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi, openapi
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser


from api.models.user import User
from api.models.message import Message
from api.serializers.userSerializers import UserSerializer
from api.serializers.messageSerializers import MessageSerializer


@method_decorator(name="create", decorator=swagger_auto_schema(
    operation_summary="Create new User",
    responses={
        400: "No name provided or it is too long",
        201: "User is created",
    },
))
@method_decorator(name="list", decorator=swagger_auto_schema(
    operation_summary="List all users",
    responses={
        201: "User is created",
    },
))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(
    operation_summary="Retrieve user data",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all",
        200: "OK",
    },
))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(
    operation_summary="Change name of user by UUID",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all; Too long name name or no name at all",
        200: "OK",
    },
))
@method_decorator(name="update", decorator=swagger_auto_schema(
    operation_summary="Replace user",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all; Too long name name or no name at all",
        200: "OK",
    },
))
@method_decorator(name="destroy", decorator=swagger_auto_schema(
    operation_summary="Delete user by UUID",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUID at all",
        204: "OK",
    },
))
@method_decorator(name="write_message", decorator=swagger_auto_schema(
    operation_summary="User can write a message to another one",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'receiver_id': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                description='receiver UUID',
            ),
            'text': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='message text'
            ),
        }),
    responses={
        404: "no user found",
        400: "Bad UUID or no UUID at all",
        201: "OK",
    },
))
@method_decorator(name="update_message", decorator=swagger_auto_schema(
    operation_summary="User can update message text, if it is written by him",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                description='message UUID',
            ),
            'text': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='new message text'
            ),
        }),
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all",
        201: "OK",
    },
))
@method_decorator(name="delete_message", decorator=swagger_auto_schema(
    operation_summary="User can delete message, if it is written by him",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                description='message UUID',
            ),
        }),
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all",
        204: "OK",
    },
))
@method_decorator(name="receive_messages", decorator=swagger_auto_schema(
    operation_summary="User can receive messages that are sent to him",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all",
        201: "OK",
    },
))
@method_decorator(name="read_sent_messages", decorator=swagger_auto_schema(
    operation_summary="User can retrieve messages  written by him",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all",
        201: "OK",
    },
))
class UserViewSet(
    viewsets.ModelViewSet,
):
    """
    Just use default request handlers, as we need user model only for tests. 

    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=['post'])
    def write_message(self, request, pk=None):
        data = JSONParser().parse(request)
        data["sender_id"] = pk
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @action(detail=True, methods=['get'])
    def receive_messages(self, request, pk=None):
        messages = Message.objects.filter(receiver_id=pk)
        serializer = MessageSerializer(messages, many=True)
        return JsonResponse(serializer.data, status=201, safe=False)

    @action(detail=True, methods=['get'])
    def read_sent_messages(self, request, pk=None):
        messages = Message.objects.filter(sender_id=pk)
        serializer = MessageSerializer(messages, many=True)
        return JsonResponse(serializer.data, status=201, safe=False)

    @action(detail=True, methods=['patch'])
    def update_message(self, request, pk=None):
        data = JSONParser().parse(request)
        message_id = data.get("id")
        new_text = data.get("text")
        if not message_id or not new_text:
            return HttpResponse(content="Bad request", status=400)
        if not new_text or new_text == "":
            return HttpResponse(
                "Bad request, no message text provided",
                status=400
            )

        try:
            message = Message.objects.get(pk=message_id)
            serializer = MessageSerializer(
                message,
                data={
                    "text": new_text},
                partial=True
            )
            initial = MessageSerializer(message)
        except Message.DoesNotExist:
            return HttpResponse("404", status=404)

        if not initial.data.get("sender_id") == pk:
            return HttpResponse("404", status=404)
        if not serializer.is_valid():
            return HttpResponse("Bad request", status=400)

        serializer.save()
        updated_message = Message.objects.get(pk=message_id)

        return JsonResponse(
            MessageSerializer(updated_message).data,
            status=200
        )
    @action(detail=True, methods=['delete'])
    def delete_message(self, request, pk=None):
        data = JSONParser().parse(request)
        message_id = data.get("id")
        if not message_id:
            return HttpResponse(content="Bad request", status=400)
        

        try:
            message = Message.objects.get(pk=message_id)
            serializer = MessageSerializer(message)
        except Message.DoesNotExist:
            return HttpResponse("404", status=404)

        if not serializer.data.get("sender_id") == pk:
            return HttpResponse("404", status=404)
        message.delete()
        return JsonResponse(
            serializer.data,
            status=204
        )
