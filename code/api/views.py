from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from django.core.exceptions import ValidationError

from api.models import Message
from api.serializers import SentMessageSerializer, RecievedMessageSerializer


class MessageView(APIView):
    """View class for message, handles HTTP requests"""

    def get(self, request):
        """
        Messages can be filtered by either 

        """
        data = JSONParser().parse(request)
        sender_id = data.get("sender_id")
        reciever_id = data.get("reciever_id")
        message_id = data.get("id")
        if not (sender_id or reciever_id):
            return HttpResponse("No sender or reciever specified", status=400)
        messages = Message.objects.all()
        try:
            if sender_id:
                messages = messages.filter(sender_id=sender_id)
            if reciever_id:
                messages = messages.filter(reciever_id=reciever_id)
            if message_id:
                messages = messages.filter(id=message_id)
        except ValidationError:
            return HttpResponse("Bad UUID of sender or reciever", status=400)

        if sender_id:
            serializer = SentMessageSerializer(messages, many=True)
        else:
            serializer= RecievedMessageSerializer(messages, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        """
        Here, we want to create a message. For this sender_id, reciever_id,
        text and date have to be specified. Message UUID is generated
        automatically, so even in case it is explicitly specified given value
        will be dropped and actuall ID is to be generated randomly. Text should 
        not be empty, date can be any, but if no other provided, is set to now.   

        """
        data = JSONParser().parse(request)
        serializer = SentMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def patch(self, request):
        """
        For updating we use PATCH HTTP method, because it is used for partial 
        update, and here we only change text. If we wanted to recreate message, 
        PUT method would be used, but here it is not the case. 
        To update message, we need to check if the user has sent this message. 
        In fact, the only way to do it is to ask user to send his UUID with the
        request and then compare with sender_id of given message. Here, we check 
        if there are message ID and user ID present in the request, then verify
        thes ID's are correct and if they are we edit the message. 
        Actually, only text is to be updated, so we simply ommit other 
        arguments. However, everything except of message UUID could be changed, 
        if we add code for it there. 

        """
        data = JSONParser().parse(request)
        sender_id = data.get("sender_id")
        message_id = data.get("id")
        new_text = data.get("text")
        if not (sender_id and message_id):
            return HttpResponse("Bad request, no message or sender specified", status=400)
        if not new_text or new_text == "":
            return HttpResponse("Bad request, no message text provided", status=400)

        try:
            message = Message.objects.get(pk=message_id)
            serializer = SentMessageSerializer(
                message, data={"text": new_text}, partial=True)
            initial = SentMessageSerializer(message)
        except Message.DoesNotExist:
            return HttpResponse("404",status=404)

        if not initial.data.get("sender_id") == sender_id:
            return HttpResponse("404", status=404)
        if not serializer.is_valid():
            return HttpResponse("Bad request", status=400)
        serializer.save()
        updated_message = Message.objects.get(pk=message_id)
        return JsonResponse(SentMessageSerializer(updated_message).data, status=200)

    def delete(self, request):
        """
        Again, to delete message user have to specify not only message id, but
        also it's own user id, in order to verify that only sender can delete 
        a message. So, we first check there are these two id's, then check if 
        this user is really a sender of this message and then delete. All other
        arguments will be ignored. 

        """

        data = JSONParser().parse(request)
        sender_id = data.get("sender_id")
        message_id = data.get("id")
        if not (sender_id and message_id):
            return HttpResponse("Bad request, no message or sender specified", status=400)
        try:
            message = Message.objects.get(pk=message_id)
            serializer = SentMessageSerializer(message)
        except Message.DoesNotExist:
            return HttpResponse("404", status=404)
        if not serializer.data.get("sender_id") == sender_id:
            return HttpResponse("404", status=404)
        message.delete()
        return JsonResponse(serializer.data, status=200)
