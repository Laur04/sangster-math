from django.urls import path

from . import views

app_name = 'discussion'

urlpatterns = (
    [
        path("discussion/", views.index, name="index"),
    ]
)