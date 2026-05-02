from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
from .models import Informe, Resultado, Conclusiones, Recomendaciones
from .serializers import (
    InformeSerializer,
    ResultadoSerializer,
    ConclusionesSerializer,
    RecomendacionesSerializer
)

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO


class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all()
    serializer_class = InformeSerializer

    @action(detail=True, methods=['get'], url_path='descargar-pdf')
    def descargar_pdf(self, request, pk=None):
        informe = self.get_object()
        resultados = informe.resultados.all()
        conclusiones = informe.conclusiones.all()
        recomendaciones = informe.recomendaciones.all()

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Encabezado
        elements.append(Paragraph(f"Informe #{informe.id}", styles['Title']))
        elements.append(Paragraph(f"Laboratorio: {informe.laboratorio}", styles['Normal']))
        elements.append(Paragraph(f"Autor: {informe.autor.username}", styles['Normal']))
        elements.append(Paragraph(f"Fecha: {informe.fecha}", styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

        # Desarrollo
        elements.append(Paragraph("Desarrollo", styles['Heading2']))
        elements.append(Paragraph(informe.desarrollo, styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

        # Análisis
        elements.append(Paragraph("Análisis", styles['Heading2']))
        elements.append(Paragraph(informe.analisis, styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

        # Resultados
        if resultados.exists():
            elements.append(Paragraph("Resultados", styles['Heading2']))
            data = [["Valor", "Unidad", "Instrumento", "Observaciones", "Fecha"]]
            for r in resultados:
                data.append([str(r.valor), r.unidad, r.instrumento, r.observaciones, str(r.fecha)])
            tabla = Table(data)
            tabla.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(tabla)
            elements.append(Spacer(1, 0.2 * inch))

        # Conclusiones
        if conclusiones.exists():
            elements.append(Paragraph("Conclusiones", styles['Heading2']))
            for c in conclusiones:
                elements.append(Paragraph(f"[{c.importancia}] {c.descripcion}", styles['Normal']))

        # Recomendaciones
        if recomendaciones.exists():
            elements.append(Paragraph("Recomendaciones", styles['Heading2']))
            for r in recomendaciones:
                elements.append(Paragraph(f"Prioridad {r.prioridad}: {r.descripcion}", styles['Normal']))

        doc.build(elements)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="informe_{informe.id}.pdf"'
        return response


class ResultadoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer


class ConclusionesViewSet(viewsets.ModelViewSet):
    queryset = Conclusiones.objects.all()
    serializer_class = ConclusionesSerializer


class RecomendacionesViewSet(viewsets.ModelViewSet):
    queryset = Recomendaciones.objects.all()
    serializer_class = RecomendacionesSerializer