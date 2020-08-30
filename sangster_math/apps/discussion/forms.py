from django import forms
from django.forms import ModelForm

from .models import Chat, Message

class ChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = [
            "name",
            "members"
        ]
        labels = {
            "name": "Chat Name:",
            "members": "Members:"
        }

class MessageForm(forms.Form):
    content = forms.CharField(max_length=400, required=True)
