from django.db import models
from django.contrib.auth.models import User

from ..utils import create_random_url

class Chat(models.Model):
    chat_id = models.CharField(max_length=30, null=False, blank=False, unique=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    members = models.ManyToManyField(User, related_name="chat_set")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.chat_id:
            self.chat_id = create_random_url()
        super().save(*args, **kwargs)

    def user_is_member(self, user):
        return user in self.members.all()

class Message(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="messages_sent")
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL, related_name="message_set")

    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    content = models.CharField(max_length=400, null=False, blank=False)

    def __str__(self):
        return "{} ({}) - {}".format(self.user.username, self.chat.name, self.content)
