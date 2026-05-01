import random
import string
import os

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from groq import Groq
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from laboratorios.models import (
    Laboratorio,
    Categoria,
    PalabraClave,
    Objetivo,
)

from .serializers import (
    LaboratorioSerializer,
    CategoriaSerializer,
    PalabraClaveSerializer,
    ObjetivoSerializer
)


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class ObjetivoViewSet(ModelViewSet):
    queryset = Objetivo.objects.all()
    serializer_class = ObjetivoSerializer
    permission_classes = [IsAuthenticated]


class PalabraClaveViewSet(ModelViewSet):
    queryset = PalabraClave.objects.all()
    serializer_class = PalabraClaveSerializer
    permission_classes = [IsAuthenticated]


class LaboratorioViewSet(viewsets.ModelViewSet):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    permission_classes = [IsAuthenticated]

    # Filtros, búsqueda y ordenamiento
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'objetivo', 'creador', 'estado', 'ra']
    search_fields = ['titulo_lab', 'codigo_lab', 'resumen', 'introduccion', 'marco_teorico']
    ordering_fields = ['titulo_lab', 'codigo_lab', 'fecha_creacion', 'fecha_actualizacion']
    ordering = ['fecha_creacion']  # orden por defecto

    def perform_create(self, serializer):
        serializer.save(
            creador=self.request.user,
            codigo_lab=self.generar_codigo()
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"mensaje": "Laboratorio creado con éxito", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    def get_queryset(self):
        queryset = Laboratorio.objects.all()
        nombre = self.request.query_params.get('nombre', None)
        if nombre:
            queryset = queryset.filter(titulo_lab__icontains=nombre)
        return queryset

    def generar_codigo(self):
        while True:
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Laboratorio.objects.filter(codigo_lab=codigo).exists():
                return codigo


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generar_contenido_ia(request):
    categoria = request.data.get('categoria', '')
    objetivos = request.data.get('objetivos', [])
    palabras_clave = request.data.get('palabras_clave', [])
    campo = request.data.get('campo', 'resumen')

    if not categoria:
        return Response({"error": "La categoría es requerida"}, status=400)

    objetivos_texto = ', '.join(objetivos) if objetivos else 'No especificados'
    palabras_texto = ', '.join(palabras_clave) if palabras_clave else 'No especificadas'

    prompts = {
        'resumen': f"""Genera un resumen académico conciso para un laboratorio de física.
Categoría: {categoria}
Objetivos: {objetivos_texto}
Palabras clave: {palabras_texto}
El resumen debe tener máximo 150 palabras, ser claro y académico. Solo responde con el resumen, sin títulos ni explicaciones.""",

        'introduccion': f"""Genera una introducción académica para un laboratorio de física.
Categoría: {categoria}
Objetivos: {objetivos_texto}
Palabras clave: {palabras_texto}
La introducción debe tener entre 200 y 300 palabras. Solo responde con la introducción, sin títulos ni explicaciones.""",

        'marco_teorico': f"""Genera un marco teórico académico para un laboratorio de física.
Categoría: {categoria}
Objetivos: {objetivos_texto}
Palabras clave: {palabras_texto}
El marco teórico debe tener entre 300 y 400 palabras, incluir conceptos físicos relevantes. Solo responde con el marco teórico, sin títulos ni explicaciones.""",
    }

    if campo not in prompts:
        return Response({"error": "Campo inválido. Usa: resumen, introduccion o marco_teorico"}, status=400)

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompts[campo]}],
            model="llama-3.3-70b-versatile",
        )
        texto_generado = chat_completion.choices[0].message.content
        return Response({"resultado": texto_generado})

    except Exception as e:
        return Response({"error": str(e)}, status=500)