from django.urls import path
from api.views import MessageView


urlpatterns = [
    path("message/", MessageView.as_view()),
]
