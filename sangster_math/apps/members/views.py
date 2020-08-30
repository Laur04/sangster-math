from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from .models import Member, Test, Score
from .forms import CreateUserForm, TestForm, ScoreForm
from ..utils import create_random_url
from ..discussion.models import Chat

def index(request):
    return render(request, 'members/index.html')

@login_required
def profile(request, member_id):
    member = Member.objects.get(member_id=member_id)
    user = member.user
    ctx = {
        "member": member,
        "user": user,
        "attendance": member.user.events_attended.all(),
        "completed_assignments": user.assignments_completed.all().order_by("-date"),
        "test_scores": user.score_set.all().order_by("-date"),
        "is_coach": request.user.groups.filter(name='coach').exists(),
        "is_user": request.user == user
    }
    return render(request, 'members/profile.html', context=ctx)

@login_required
def list_students(request):
    if request.user.groups.filter(name="coach").exists():
        students = Group.objects.get(name="students").user_set.all()
        return render(request, "members/list.html", context={"students": students})
    else:
        raise PermissionDenied

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['student_email'].endswith('@fcpsschools.net'):
                new_user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['parent_email'],
                    form.cleaned_data['password_one'])
            else:
                new_user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['student_email'],
                    form.cleaned_data['password_one'])
            new_user.first_name = form.cleaned_data['student_first_name']
            new_user.last_name = form.cleaned_data['student_last_name']
            new_member = Member(
                user=new_user, 
                member_id=create_random_url(),
                parent_first_name=form.cleaned_data["parent_first_name"],
                parent_last_name=form.cleaned_data["parent_last_name"],
                parent_email=form.cleaned_data["parent_email"],
                student_id=form.cleaned_data["student_id"]
                )
            new_user.groups.add(Group.objects.get_or_create(name="students")[0])
            new_user.save()
            new_member.save()
            chat_members_list = [new_user]
            for u in Group.objects.get(name="coach").user_set.all():
                chat_members_list.append(u)
            new_chat = Chat(
                chat_id=create_random_url(), 
                name="{} {} Private Chat".format(new_user.first_name, new_user.last_name))
            new_chat.save()
            for m in chat_members_list:
                new_chat.members.add(m)
            new_chat.save()
            return redirect(reverse('login'))
        return render(request, 'members/create.html', context={'form': form})
    else:
        form = CreateUserForm()
        return render(request, 'members/create.html', context={'form': form}) 

@login_required
def test_list(request):
    if request.user.groups.filter(name="coach").exists():
        tests = {t: t.scores_set.all().order_by("-score") for t in Test.objects.all().order_by("-date")}
        return render(request, "members/test_list.html", context={"tests": tests})
    else:
        raise PermissionDenied

@login_required
def edit_test(request, test_id):
    if request.user.groups.filter(name="coach").exists():
        test = Test.objects.get(test_id=test_id)
        score_forms = []
        if request.method == 'POST':
            test_form = TestForm(request.POST, instance=test)
            score_forms = [ScoreForm(request.POST, instance=s) for s in test.scores_set.all()]
            if all_forms_valid(test_form, score_forms):
                test_form.save()
                for f in score_forms:
                    f.save()
                return redirect(reverse('members:test_list'))
            else:
                return render(request, 'members/edit_create.html', context={"test_form": test_form, "score_forms": score_forms})
        else:
            ctx = {
                "test_form": TestForm(instance=test),
                "score_forms": [ScoreForm(instance=s) for s in test.scores_set.all()]
            }
            return render(request, "members/edit_create.html", context=ctx)
    else:
        raise PermissionDenied

@login_required
def add_test(request):
    if request.user.groups.filter(name="coach").exists():
        new_test = Test(test_id=create_random_url(), points=0)
        new_test.save()
        for s in Group.objects.get(name="students").user_set.all():
            new_score = Score(user=s, score=0, test=new_test)
            new_score.save()
        return edit_test(request, new_test.test_id)
    else:
        raise PermissionDenied

def all_forms_valid(test_form, score_forms):
    test_valid = test_form.is_valid()
    score_valid = True
    for f in score_forms:
        if not f.is_valid():
            score_valid = False
    return test_valid and score_valid
