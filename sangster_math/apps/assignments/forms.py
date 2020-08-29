from django import forms
from django.forms import ModelForm

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "assignment_link",
            "answer_link",
            "answer_post_time"
        ]
        labels = {
            "title": "Post Title:",
            "content": "Post Description:",
            "assignment_link": "Link to Assignment:",
            "answer_link": "Link to Answers:",
            "answer_post_time": "Time to Post Answers (mm/dd/yy hh:mm):"
        }

    def is_valid(self):
        valid = super().is_valid()

        not_given_time = self.cleaned_data["answer_link"] is not None and self.cleaned_data["answer_post_time"] is None
        if not_given_time:
            self.add_error('answer_post_time', "You must specify a time to make the answers available.")

        return valid and not not_given_time
