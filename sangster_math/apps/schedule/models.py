from django.db import models
from django.contrib.auth.models import User, Group

from ..utils import create_random_url

import datetime

class Day(models.Model):
    DAYS = [(0, "Sunday"), (1, "Monday"), (2, "Tuesday"), (3, "Wednesday"), (4, "Thursday"), (5, "Friday"), (6, "Saturday")]

    date = models.DateField(blank=False, null=False, unique=True)
    month = models.CharField(max_length=30, blank=False, null=False)
    weekday = models.CharField(max_length=30, blank=False, null=False, choices=DAYS)

    def __str__(self):
        return str(self.date)

    def is_current(self):
        return datetime.datetime.today() == self.date

    def get_weekday_num(self):
        DAYS = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}
        return DAYS[self.weekday]

class Event(models.Model):
    event_id = models.CharField(max_length=30, blank=False, null=False, unique=True)

    day = models.ForeignKey(Day, null=True, on_delete=models.SET_NULL, related_name="event_set")
    time = models.TimeField(blank=False, null=False)
    name = models.CharField(max_length=40, blank=False, null=False)

    attendance_taken = models.BooleanField(default=False)
    attendees = models.ManyToManyField(User, related_name="events_attended")
    users_attending = models.ManyToManyField(User, related_name="events_marked_attending")

    def __str__(self):
        return self.name + " - " + str(self.day)

    def save(self, *args, **kwargs):
        if not self.event_id:
            self.event_id = create_random_url()
        super().save(*args, **kwargs)

    def is_past(self):
        return datetime.date.today() > self.day.date

    def users_attending_pretty(self):
        if self.users_attending.all():
            return "".join(["{} {} ({}), ".format(u.first_name, u.last_name, u.username) for u in self.users_attending.all()])
        else:
            return "None"

    def users_attended_pretty(self):
        if self.attendees.all():
            return "".join(["{} {} ({}), ".format(u.first_name, u.last_name, u.username) for u in self.attendees.all()])
        else:
            return "None"

    def user_attending(self, user):
        return user in self.users_attending.all()
