from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from ..members.models import Member
from .models import Day, Event
from .forms import EventForm, AttendanceForm

import datetime

def calendar_redirect(request):
    month = "September"
    if datetime.date.today() > datetime.date(2020, 9, 1):
        month = datetime.datetime.today().strftime('%B')
    return redirect(reverse('schedule:calendar_by_month', args=[month]))

def calendar(request, month):
    MONTH_STR_TO_NUM = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    MONTH_NUM_TO_STR = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

    prev_month = None
    next_month = None
    if month != "September":
        if month == "January":
            prev_month = "December"
        else:
            prev_month = MONTH_NUM_TO_STR[MONTH_STR_TO_NUM[month] - 1]
    if month != "August":
        if month == "December":
            next_month = "January"
        else:
            next_month = MONTH_NUM_TO_STR[MONTH_STR_TO_NUM[month] + 1]

    weeks = []
    all_days = Day.objects.filter(month=month).order_by("date")
    
    day_one = all_days[0].get_weekday_num()
    week_one = [None for d in range(day_one)]
    for x in range(7 - day_one):
        week_one.append([all_days[x], [[e, e.user_attending(request.user)] for e in all_days[x].event_set.all().order_by("time")]])
    next_week_start = 7 - day_one

    weeks.append(week_one)
    while next_week_start + 6 <= len(all_days):
        weeks.append([[d, [[e, e.user_attending(request.user)] for e in d.event_set.all().order_by("time")]] for d in all_days[next_week_start: next_week_start + 7]])
        next_week_start += 7

    last_week = [[d, [[e, e.user_attending(request.user)] for e in d.event_set.all().order_by("time")]] for d in all_days[next_week_start:len(all_days)]]
    if last_week:
        for d in range(7 - len(last_week)):
            last_week.append(None)
        weeks.append(last_week)

    ctx = {
        "is_coach": request.user.groups.filter(name='coach').exists(),
        "weeks": weeks,
        "prev_month": prev_month,
        "next_month": next_month,
        "month": month
    }
    return render(request, 'schedule/index.html', context=ctx)

@login_required
def add_event(request):
    if request.user.groups.filter(name='coach').exists():
        if request.method == "POST":
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save()
                send_mail(
                    "New Sangster Math Club Event: {}".format(event.name),
                    "A new event on {} at {} was just scheduled. View the event and mark your availability at https://sangster_math_club.herokuapp.com/schedule/".format(event.day, event.time),
                    settings.DEFAULT_FROM_EMAIL,
                    Member.create_email_list(),
                    fail_silently=True
                )
                return redirect(reverse("schedule:calendar"))
            return render(request, 'schedule/edit_create.html', context={"form": form})
        form = EventForm()
        return render(request, 'schedule/edit_create.html', context={"form": form})
    else:
        raise PermissionDenied

@login_required
def remove_event(request, event_id):
    if request.user.groups.filter(name='coach').exists():
        event = get_object_or_404(Event, event_id=event_id)
        event.delete()
        return redirect(reverse("schedule:calendar"))
    else:
        raise PermissionDenied

@login_required
def edit_event(request, event_id):
    if request.user.groups.filter(name='coach').exists():
        event = get_object_or_404(Event, event_id=event_id)
        if request.method == "POST":
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect(reverse("schedule:calendar"))
            return render(request, 'schedule/edit_create.html', context={"form": form})
        form = EventForm(instance=event)
        return render(request, 'schedule/edit_create.html', context={"form": form})
    else:
        raise PermissionDenied

@login_required
def mark(request, direction, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    if direction == "add":
        event.users_attending.add(request.user)
    elif direction == "remove":
        event.users_attending.remove(request.user)
    event.save()
    return redirect(reverse("schedule:calendar"))

@login_required
def attendance(request, event_id):
    if request.user.groups.filter(name='coach').exists():
        event = get_object_or_404(Event, event_id=event_id)
        if request.method == 'POST':
            form = AttendanceForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                event.attendance_taken = True
                event.save()
                return redirect(reverse("schedule:calendar"))
            return render(request, "schedule/attendance.html", context={"form": form})
        form = AttendanceForm(instance=event)
        return render(request, "schedule/attendance.html", context={"form": form})
    else:
        raise PermissionDenied
