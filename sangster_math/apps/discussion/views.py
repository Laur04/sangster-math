from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from ..members.models import Member
from .models import Chat, Message
from .forms import ChatForm, MessageForm

@login_required
def index(request):
    ctx = {
        "chat_list": request.user.chat_set.all(),
        "is_coach": request.user.groups.filter(name='coach').exists(),
        "personal_email_list": Member.create_email_string(),
        "school_email_list": Member.create_school_email_string()
    }
    return render(request, 'discussion/index.html', context=ctx)

@login_required
def view_chat(request, chat_id):
    chat = get_object_or_404(Chat, chat_id=chat_id)
    if chat.user_is_member(request.user):
        emails = []
        members = []
        for user in chat.members.all():
            if not user.groups.filter(name='coach').exists():
                if not user.member.same_email():
                    emails.append(user.email)
                emails.append(user.member.parent_email)
            members.append("{} {}".format(user.first_name, user.last_name))
        ctx = {
            "messages": [[m, m.user == request.user] for m in chat.message_set.all().order_by("date")],
            "is_coach": request.user.groups.filter(name='coach').exists(),
            "chat": chat,
            "form": None,
            "emails": ",".join(emails),
            "members": ", ".join(members)
        }
        if request.method == 'POST':
            form = MessageForm(request.POST)
            ctx["form"] = form
            if form.is_valid():
                new_message = Message(
                    user=request.user,
                    chat=chat,
                    content=form.cleaned_data["content"]
                )
                new_message.save()
                return redirect(reverse("discussion:view_chat", args=[chat_id]))
        else:
            ctx["form"] = MessageForm()
        return render(request, "discussion/view.html", context=ctx)
    else:
        raise PermissionDenied

@login_required
def edit_chat(request, chat_id):
    if request.user.groups.filter(name='coach').exists():
        chat = get_object_or_404(Chat, chat_id=chat_id)
        if request.method == 'POST':
            form = ChatForm(request.POST, instance=chat)
            if form.is_valid():
                form.save()
                return redirect(reverse("discussion:index"))
            return render(request, "discussion/create_edit.html", context={"form": form})
        form = ChatForm(instance=chat)
        return render(request, "discussion/create_edit.html", context={"form": form})
    else:
        raise PermissionDenied

@login_required
def add_chat(request):
    if request.user.groups.filter(name='coach').exists():
        if request.method == 'POST':
            form = ChatForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse("discussion:index"))
            return render(request, "discussion/create_edit.html", context={"form": form})
        form = ChatForm()
        return render(request, "discussion/create_edit.html", context={"form": form})
    else:
        raise PermissionDenied
