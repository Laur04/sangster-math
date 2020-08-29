from django.urls import path

from . import views

app_name = 'schedule'

urlpatterns = (
    [
        path("schedule/attendance/<slug:event_id>/", views.attendance, name="attendance"),
        path("schedule/", views.calendar_redirect, name="calendar"),
        path("schedule/event/add/", views.add_event, name="add_event"),
        path("schedule/delete/<slug:event_id>/", views.remove_event, name="remove_event"),
        path("schedule/edit/<slug:event_id>/", views.edit_event, name="edit_event"),
        path("schedule/<direction>/<slug:event_id>/", views.mark, name="mark"),
        path("schedule/<month>/", views.calendar, name="calendar_by_month"),
    ]
)