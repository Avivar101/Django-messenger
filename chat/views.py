import json

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render


# view of the chat-room entry page
from django.utils.safestring import mark_safe


@login_required
def index(request):
    return render(request, "chat/index.html")


# chat-room page
@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "user": request.user.username
    })


class Register(FormView):
    template_name = "chat/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('chat:home')

    # redirect once the user has registered
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form) 
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('chat:home')
        return super(Register, self).get(*args, **kwargs)
    

class Login(LoginView):
    template_name = "chat/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('chat:home')
    





