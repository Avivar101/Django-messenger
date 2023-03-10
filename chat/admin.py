from django.contrib import admin

from .models import Message, UserModel

admin.site.register(UserModel)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'content')


admin.site.register(Message, MessageAdmin)