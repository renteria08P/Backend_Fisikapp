from django.urls import include, path

urlpatterns = [

    path(
        "resources/",
        include("mobile.resources.urls"),
    ),

    path(
        "simulation/",
        include("mobile.simulation.urls"),
    ),

]