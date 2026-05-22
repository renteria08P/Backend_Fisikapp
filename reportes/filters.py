import django_filters

from .models import ReporteLaboratorio


class HistorialReporteFilter(django_filters.FilterSet):

    fecha = django_filters.DateFilter(
        field_name='fecha_creacion'
    )

    class Meta:

        model = ReporteLaboratorio

        fields = ['fecha']