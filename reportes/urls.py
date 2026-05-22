from django.urls import path

from .views import HistorialReportesDocenteView


urlpatterns = [

    path(
        'historial/',
        HistorialReportesDocenteView.as_view(),
        name='historial-reportes-docente'
    ),
]