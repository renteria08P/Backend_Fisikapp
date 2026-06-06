from rest_framework import serializers

from .models import ReporteLaboratorio


class HistorialReporteSerializer(serializers.ModelSerializer):

    laboratorio_nombre = serializers.CharField(
        source='laboratorio_profesor.laboratorio.titulo_lab'
    )

    estudiantes_info = serializers.SerializerMethodField()

    url_reporte_estudiante = serializers.SerializerMethodField()

    reporte_docente_info = serializers.SerializerMethodField()

    url_informe_final = serializers.SerializerMethodField()

    class Meta:

        model = ReporteLaboratorio

        fields = [
            'id',
            'laboratorio_nombre',
            'estado_informe',
            'fecha_creacion',
            'estudiantes_info',
            'url_reporte_estudiante',
            'reporte_docente_info',
            'url_informe_final',
        ]

    # ======================================
    # ESTUDIANTES
    # ======================================

    def get_estudiantes_info(self, obj):

        estudiantes = obj.estudiantes.all()

        lista = []

        nombres = []

        for estudiante in estudiantes:

            nombres.append(estudiante.nombre)

            lista.append({
                "id": estudiante.id,
                "nombre": estudiante.nombre,
                "codigo": estudiante.identificacion,
                "correo": estudiante.correo
            })

            return {
            "lista_detallada": lista
        }
    # ======================================
    # PDF ESTUDIANTE
    # ======================================

    def get_url_reporte_estudiante(self, obj):

        request = self.context.get('request')

        if obj.reporte_estudiante:
            return request.build_absolute_uri(
                obj.reporte_estudiante.url
            )

        return None

    # ======================================
    # OBSERVACIONES DOCENTE
    # ======================================

    def get_reporte_docente_info(self, obj):

        if obj.observaciones_docente:

            return {
                "tiene_observaciones": True,
                "observaciones": obj.observaciones_docente
            }

        return {
            "tiene_observaciones": False,
            "observaciones": ""
        }

    # ======================================
    # INFORME FINAL
    # ======================================

    def get_url_informe_final(self, obj):

        request = self.context.get('request')

        if obj.informe_final:
            return request.build_absolute_uri(
                obj.informe_final.url
            )

        return None