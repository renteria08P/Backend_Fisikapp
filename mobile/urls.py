from django.urls import path
from .views import MobileResourceView

urlpatterns = [

    path(
        "resources/<int:assignment_id>/",
        MobileResourceView.as_view(),
        name="mobile-resource",
    ),

]