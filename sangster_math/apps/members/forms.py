from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Member, Test, Score

class CreateUserForm(forms.Form):
    username = forms.SlugField(label="Username (You can use letters, numbers and underscores):", min_length=4, max_length=20, required=True)
    student_first_name = forms.CharField(label="Student First Name:", max_length=40, required=True)
    student_last_name = forms.CharField(label="Student Last Name:", max_length=40, required=True)
    student_email = forms.EmailField(label="Student Email:", required=True)
    student_id = forms.CharField(label="Student ID:", max_length=7, required=True)

    parent_first_name = forms.CharField(label="Parent First Name:", max_length=40, required=True)
    parent_last_name = forms.CharField(label="Parent Last Name:", max_length=40, required=True)
    parent_email = forms.EmailField(label="Parent Email:", required=True)

    student_grade = forms.BooleanField(label="I am in 6th grade at Sangster Elementary.", required=True)

    password_one = forms.CharField(label="Password:", min_length=5, max_length=20, widget=forms.PasswordInput)
    password_two = forms.CharField(label="Reenter Password:", min_length=5, max_length=20, widget=forms.PasswordInput)

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid

        same = self.cleaned_data["password_one"] == self.cleaned_data["password_two"]
        if not same:
            self.add_error('password_two', 'Passwords do not match.')
        
        not_unique_username = User.objects.filter(username=self.cleaned_data['username']).exists()
        if not_unique_username:
            self.add_error('username', "A user with that username already exists.")
        
        not_unique_id = Member.objects.filter(student_id=self.cleaned_data['student_id']).exists()
        if not_unique_id:
            self.add_error('student_id', "A user with that Student ID already exists.")

        return valid and same and not not_unique_username and not not_unique_id

class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = [
            "title",
            "points"
        ]
        labels = {
            "title": "Test Title:",
            "points": "Total Possible Points"
        }

class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = [
            "score"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["score"].label = self.instance.user
