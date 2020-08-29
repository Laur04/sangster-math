from django.urls import path

from . import views

app_name = 'members'

urlpatterns = (
    [
        path("", views.index, name="index"),
        path("profile-list/", views.list_students, name="list_students"),
        path("profile/<slug:member_id>/", views.profile, name="profile"),
        path("signup/", views.signup, name="signup"),
        path("test/list/", views.test_list, name="test_list"),
        path("test/edit/<slug:test_id>/", views.edit_test, name="edit_test"),
        path("test/add/", views.add_test, name="add_test"),
    ]
)