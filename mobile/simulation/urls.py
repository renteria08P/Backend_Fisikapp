from django.urls import path

from .views import (
    SimulationConfigAPIView,
    SimulationResultAPIView,
)

urlpatterns = [

    path(
        "<int:assignment_id>/",
        SimulationConfigAPIView.as_view(),
        name="simulation-config",
    ),

    path(
        "<int:assignment_id>/results/",
        SimulationResultAPIView.as_view(),
        name="simulation-result",
    ),

]