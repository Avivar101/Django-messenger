from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username
    


class Message(models.Model):
    author = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by("-timestamp").all()[:10]
