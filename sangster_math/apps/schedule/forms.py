from django import forms
from django.forms import ModelForm

from .models import Day, Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            "day",
            "time",
            "name"
        ]
        labels = {
            "day": "Event Date:",
            "time": "Event Time (hh:mm:ss):",
            "name": "Event Title:"
        }

class AttendanceForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            "attendees"
        ]
        labels = {
            "attendees": "Mark those present:"
        }
