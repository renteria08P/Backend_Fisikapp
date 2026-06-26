import django_filters
from django.db.models import Q

from .models import ReporteLaboratorio


class HistorialReporteFilter(django_filters.FilterSet):

    fecha = django_filters.DateFilter(
        field_name="fecha_creacion"
    )

    estudiante = django_filters.CharFilter(
        method="filtrar_estudiante"
    )

    laboratorio = django_filters.CharFilter(
        field_name="laboratorio__plantilla__titulo",
        lookup_expr="icontains"
    )

    class Meta:
        model = ReporteLaboratorio
        fields = [
            "fecha",
            "estudiante",
            "laboratorio",
        ]

    def filtrar_estudiante(self, queryset, name, value):
        return queryset.filter(
            estudiantes__nombre__icontains=value
        ).distinct()