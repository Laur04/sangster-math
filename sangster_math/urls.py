from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("django.contrib.auth.urls")),
        path("", include("sangster_math.apps.assignments.urls", namespace="assignments")),
        path("", include("sangster_math.apps.discussion.urls", namespace="discussion")),
        path("", include("sangster_math.apps.members.urls", namespace="members")),
        path("", include("sangster_math.apps.schedule.urls", namespace="schedule")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
