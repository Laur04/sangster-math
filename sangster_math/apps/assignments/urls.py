from django.urls import path

from . import views

app_name = 'assignments'

urlpatterns = (
    [
        path("assignments/", views.index, name="index"),
        path("assignments/edit/<slug:post_id>/", views.edit_post, name="edit"),
        path("assignments/create/", views.create_post, name="create"),
        path("assignments/toggle/<slug:post_id>/<direction>/", views.toggle, name="toggle"),
    ]
)
