from django.contrib import admin
from django.urls import path, include

from chat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("chat/", include("chat.urls", namespace="chat")),
]
