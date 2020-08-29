from django.db import models
from django.contrib.auth.models import User

from ..utils import create_random_url

class Member(models.Model):
    user = models.OneToOneField(User, related_name='member', unique=True, on_delete=models.CASCADE)
    member_id = models.CharField(max_length=30, null=False, blank=False, unique=True)

    parent_first_name = models.CharField(max_length=40, null=False, blank=False)
    parent_last_name = models.CharField(max_length=40, null=False, blank=False)
    parent_email = models.CharField(max_length=40, null=False, blank=False)

    student_id = models.CharField(max_length=7, null=False, blank=False, unique=True)

    def __str__(self):
        return self.user.username

    def get_school_email(self):
        return self.student_id + '@fcpsschools.net'  

    def same_email(self):
        return self.user.email == self.parent_email

    @staticmethod
    def create_email_list():
        email_list = []
        for m in Member.objects.all():
            email_list.append(m.parent_email)
            if not m.same_email():
                email_list.append(m.user.email)
        return email_list

    @staticmethod
    def create_school_email_list():
        return [m.get_school_email() for m in Member.objects.all()]

class Test(models.Model):
    test_id = models.CharField(max_length=30, null=False, blank=False, unique=True)

    title = models.CharField(max_length=40, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.title

    def save_initial(self, *args, **kwargs):
        self.test_id = create_random_url()
        super().save(*args, **kwargs)

class Score(models.Model):
    score = models.IntegerField(blank=False, null=False)
    
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="score_set")
    date = models.DateTimeField(auto_now_add=True)
    test = models.ForeignKey(Test, null=True, on_delete=models.SET_NULL, related_name="scores_set")

    def __str__(self):
        return self.user.username + " - " + self.test.title

    def get_percentage(self):
        if self.test.points != 0:
            return "{:.1%}".format(self.score / self.test.points)
        else:
            return "0%" 
    