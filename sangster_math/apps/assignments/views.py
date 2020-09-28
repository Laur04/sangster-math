from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMessage

from ..members.models import Member
from .models import Post
from .forms import PostForm

@login_required
def index(request):
    is_coach = request.user.groups.filter(name='coach').exists()
    posts = [[p, p.user_completed(request.user)] for p in Post.objects.all().order_by("-date")]
    return render(request, 'assignments/index.html', context={'posts': posts, 'is_coach': is_coach})

@login_required
def edit_post(request, post_id):
    if request.user.groups.filter(name='coach').exists():
        post = get_object_or_404(Post, post_id=post_id)
        if request.method == 'POST':
            post_form = PostForm(request.POST, instance=post)
            if post_form.is_valid():
                post_form.save({"user": request.user, "initial": False})
                return redirect(reverse('assignments:index'))
            return render(request, 'assignments/edit_create.html', context={"post_form": post_form})
        post_form = PostForm(instance=post)
        return render(request, 'assignments/edit_create.html', context={"post_form": post_form})
    else:
        raise PermissionDenied

@login_required
def create_post(request):
    if request.user.groups.filter(name='coach').exists():
        if request.method == 'POST':
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save({"user": request.user})
                email = EmailMessage(
                    "Sangster Math Club Announcement/Assignment: {}".format(post.title),
                    post.content + '\n\n View this post here: https://sangster-math-club.herokuapp.com/assignments/#{}'.format(post.post_id),
                    settings.DEFAULT_FROM_EMAIL,
                    ['sangstermath@gmail.com'],
                    Member.create_email_list(),
                    reply_to=['pmd7211@gmail.com']
                )
                email.send(fail_silently=True)
                return redirect(reverse('assignments:index'))
            return render(request, 'assignments/edit_create.html', context={"post_form": post_form})
        post_form = PostForm()
        return render(request, 'assignments/edit_create.html', context={"post_form": post_form})
    else:
        raise PermissionDenied

@login_required
def toggle(request, post_id, direction):
    assignment = get_object_or_404(Post, post_id=post_id)
    if direction == "add":
        assignment.users_completed.add(request.user)
    elif direction == "remove":
        assignment.users_completed.remove(request.user)
    assignment.save()
    return redirect(reverse("assignments:index"))
