from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from api.models.user import User
from api.serializers.userSerializers import UserSerializer


@method_decorator(name="create", decorator=swagger_auto_schema(
    operation_summary="Create new User",
    responses={
        400: "No name provided or it is too long",
        201: "User is created",
    }
))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(
    operation_summary="Retrieve user data",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all",
        200: "OK",
    }
))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(
    operation_summary="Change name of user by UUID",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all; Too long name name or no name at all",
        200: "OK",
    }
))
@method_decorator(name="update", decorator=swagger_auto_schema(
    operation_summary="Replace user",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all; Too long name name or no name at all",
        200: "OK",
    }
))
@method_decorator(name="destroy", decorator=swagger_auto_schema(
    operation_summary="Change name of user by UUID",
    responses={
        404: "no user found",
        400: "Bad UUID or no UUD at all",
        204: "OK",
    }
))

class UserViewSet(
    viewsets.ModelViewSet,
):
    """
    Just use default request handlers, as we need user model only for tests. 

    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
