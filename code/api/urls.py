from django.conf.urls import url
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.views.userViews import UserViewSet

openapi_info = openapi.Info(
    title="Messenger API",
    default_version='v2',
    description="Second version of simple RESTful messenger",
)
schema_view = get_schema_view(
    openapi_info,
    public=True,
)

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
urlpatterns = [
    
    url(
        r'^swagger/$',
        schema_view.with_ui(
            'swagger',
        ),
        name='schema-swagger-ui',
    ),

]
urlpatterns += router.urls