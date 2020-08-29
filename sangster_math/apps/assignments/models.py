from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone

from ..utils import create_random_url

import datetime

class Post(models.Model):
    post_id = models.SlugField(max_length=30, blank=False, null=False, unique=True)

    created_by = models.ForeignKey(User, null=True, related_name="posts_created", on_delete=models.SET_NULL)

    title = models.CharField(max_length=40, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=4000, blank=False, null=False)

    assignment_link = models.URLField(blank=True, null=True)
    answer_link = models.URLField(blank=True, null=True)
    answer_post_time = models.DateTimeField(blank=True, null=True)

    users_completed = models.ManyToManyField(User, related_name="assignments_completed")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.post_id:
            self.post_id = create_random_url()
            self.created_by = kwargs.pop('user', None)
        super().save(*args, **kwargs)

    def user_completed(self, user):
        if self.is_assignment() and user.groups.filter(name="students").exists():
            return user in self.users_completed.all()
        else:
            return None

    def is_assignment(self):
        return self.assignment_link is not None

    def answers_showing(self):
        return self.answer_post_time < timezone.now()

    def users_completed_pretty(self):
        if self.users_completed.all():
            return "".join(["{} {} ({})\n".format(u.first_name, u.last_name, u.username) for u in self.users_completed.all()])
        else:
            return "None"
