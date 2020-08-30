from django.urls import path

from . import views

app_name = 'discussion'

urlpatterns = (
    [
        path("discussion/", views.index, name="index"),
        path("discussion/view/<slug:chat_id>/", views.view_chat, name="view_chat"),
        path("discussion/edit/<slug:chat_id>/", views.edit_chat, name="edit_chat"),
        path("discussion/add/", views.add_chat, name="add_chat"),
    ]
)
