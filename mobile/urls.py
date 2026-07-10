from django.urls import include, path

from .group_views import (
    join_group,
    my_groups,
    group_assignments,
)
from .ar_views import MobileARConfigAPIView

from .views import MobileResourceView

from .submission_views import MobileUnifiedSubmissionAPIView

urlpatterns = [

    path(
        "resources/<int:assignment_id>/",
        MobileResourceView.as_view(),
        name="mobile-resource",
    ),

    path(
        "groups/join/",
        join_group,
        name="mobile-groups-join"
    ),

    path(
        "groups/",
        my_groups,
        name="mobile-my-groups"
    ),

    path(
        "groups/<int:grupo_id>/assignments/",
        group_assignments,
        name="mobile-group-assignments"
    ),

    path(
        "ar/<int:ar_id>/",
        MobileARConfigAPIView.as_view(),
        name="mobile-ar-config"
    ),

    # Mantener viejo si todavía existe para compatibilidad:
    path(
        "simulation/",
        include("mobile.simulation.urls"),
    ),

    path(
        "assignments/<int:assignment_id>/submit/",
        MobileUnifiedSubmissionAPIView.as_view(),
        name="mobile-unified-submit"
    ),

]