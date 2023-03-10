from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.Register.as_view(), name="register"),
    path("login", views.Login.as_view(), name="login"),
    
    path("home", views.index, name="home"),
    path("<str:room_name>/", views.room, name="room"),
]