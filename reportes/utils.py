from django.template.loader import get_template

from xhtml2pdf import pisa

from io import BytesIO

from django.core.files.base import ContentFile


def generar_pdf_reporte(reporte):

    template = get_template(
        'reportes/reporte_estudiante.html'
    )

    html = template.render({
        'laboratorio': reporte.laboratorio_profesor.laboratorio.titulo_lab,
        'profesor': reporte.laboratorio_profesor.profesor.nombre,
        'fecha': reporte.fecha_creacion,
        'estudiantes': reporte.estudiantes.all(),
        'observaciones': reporte.observaciones_docente
    })

    resultado = BytesIO()

    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")),
        resultado
    )

    if not pdf.err:

        nombre_pdf = f"reporte_{reporte.id}.pdf"

        reporte.informe_final.save(
            nombre_pdf,
            ContentFile(resultado.getvalue()),
            save=True
        )

        return reporte.informe_final.url

    return None