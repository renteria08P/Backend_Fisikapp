from django.urls import include, path

from .views import MobileResourceView

urlpatterns = [

    path(
        "resources/<int:assignment_id>/",
        MobileResourceView.as_view(),
        name="mobile-resource",
    ),

    path(
        "simulation/",
        include("mobile.simulation.urls"),
    ),

]