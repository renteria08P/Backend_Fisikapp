import random
import string
import os
import requests 

from laboratorios.models import Etapa, ProgresoEstudiante
from datetime import date
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  filters
from rest_framework.decorators import action
from django.db import transaction
from users.models import Users
import pandas as pd
from inscripciones.models import Inscripcion
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
from inscripciones.serializers import InscripcionSerializer
from users.permissions import IsProfesor

from rest_framework.decorators import (
    api_view,
    permission_classes,
    action
    
)

from laboratorios.models import (
    Laboratorio,
    Categoria,
    PalabraClave,
    Objetivo,
    LaboratorioProfesor,
    Etapa,              # ← NUEVO
    ProgresoEstudiante,
)

from .serializers import (
    LaboratorioSerializer,
    CategoriaSerializer,
    PalabraClaveSerializer,
    ObjetivoSerializer,
    LaboratorioProfesorSerializer
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


class LaboratorioViewSet(ModelViewSet):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    permission_classes = [IsAuthenticated]

    # Filtros, búsqueda y ordenamiento
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'objetivo', 'creador', 'estado', 'ra']
    search_fields = ['titulo_lab', 'resumen', 'introduccion', 'marco_teorico']
    ordering_fields = ['titulo_lab', 'fecha_creacion', 'fecha_actualizacion']
    ordering = ['fecha_creacion']  # orden por defecto

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "mensaje": "Laboratorio creado con éxito",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        ) 

    def get_queryset(self):          
        queryset = Laboratorio.objects.all()
        nombre = self.request.query_params.get('nombre', None)  
        if nombre:
            queryset = queryset.filter(titulo_lab__icontains=nombre)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(creador=self.request.user)


    def get_permissions(self):
        if self.action == "cargar_estudiantes_excel":
            return [IsAuthenticated(), IsProfesor()]

        return [IsAuthenticated()]

# =========================================================
# LABORATORIO PROFESOR
# =========================================================

class LaboratorioProfesorViewSet(ModelViewSet):

    queryset = LaboratorioProfesor.objects.all()

    serializer_class = LaboratorioProfesorSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = [
        'profesor',
        'estado',
        'generado_ia'
    ]

    search_fields = [
        'codigo_lab',
        'laboratorio__titulo_lab'
    ]

    ordering_fields = [
        'fecha_creacion',
        'fecha_actualizacion'
    ]

    ordering = ['-fecha_creacion']


    def generar_codigo(self):

        while True:

            codigo = ''.join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=8
                )
            )

            if not LaboratorioProfesor.objects.filter(
                codigo_lab=codigo
            ).exists():

                return codigo
            

    def perform_create(self, serializer):

        laboratorio = serializer.validated_data['laboratorio']

        serializer.save(
            profesor=self.request.user,
            codigo_lab=self.generar_codigo(),

            # COPIA AUTOMÁTICA
            resumen=laboratorio.resumen,
            prologo=laboratorio.prologo,
            introduccion=laboratorio.introduccion,
            marco_teorico=laboratorio.marco_teorico,
        )

    @action(detail=False, methods=['get'])
    def mis_laboratorios(self, request):
        qs = self.queryset.filter(profesor=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['get'])
    def estudiantes(self, request, pk=None):

        laboratorio = self.get_object()

        inscripciones = Inscripcion.objects.filter(
            laboratorio=laboratorio
        )

        estudiantes = []

        for inscripcion in inscripciones:

            estudiantes.append({
                "id": inscripcion.usuario.id,
                "nombre": inscripcion.usuario.nombre,
                "correo": inscripcion.usuario.correo,
                "fecha_inscripcion": inscripcion.fecha_inscripcion
            })

        return Response(estudiantes)
    
   
    @action(detail=True, methods=['post'])
    def generar_con_ia(self, request, pk=None):
        lab = self.get_object()
    
        try:
            ia = requests.post(
                "https://agentes-ia-9heysq.fly.dev/generar-contenido",
                json={
                    "categoria": str(lab.categoria),
                    "objetivo": str(lab.objetivo),
                    "palabras_clave": str(lab.titulo_lab)
                },
                timeout=30
            ).json()
        except:
            return Response({"error": "No se pudo conectar con la IA"}, status=500)

        lab.resumen = ia.get("resumen", "")
        lab.prologo = ia.get("prologo", "")
        lab.introduccion = ia.get("introduccion", "")
        lab.marco_teorico = ia.get("marco_teorico", "")
        lab.generado_ia = True
        lab.save()

        return Response({"mensaje": "Contenido generado", "data": LaboratorioProfesorSerializer(lab).data})
    

    @action(detail=True, methods=['get'])
    def progreso(self, request, pk=None):
        laboratorio = self.get_object()
        etapas = Etapa.objects.filter(laboratorio=laboratorio).order_by('orden')
        total = etapas.count()
        completadas = 0
        resultado = []

        for etapa in etapas:
            prog = ProgresoEstudiante.objects.filter(
                estudiante=request.user, etapa=etapa
            ).first()
            hecho = prog.completada if prog else False
            if hecho:
                completadas += 1
            resultado.append({"etapa_id": etapa.id, "nombre": etapa.nombre, "completada": hecho})

        return Response({
            "porcentaje": int((completadas / total) * 100) if total > 0 else 0,
            "etapas": resultado
        })


    @action(detail=True, methods=['post'], url_path='etapas/(?P<etapa_id>[^/.]+)/completar')
    def completar_etapa(self, request, pk=None, etapa_id=None):
        laboratorio = self.get_object()
        try:
            etapa = Etapa.objects.get(id=etapa_id, laboratorio=laboratorio)
        except Etapa.DoesNotExist:
            return Response({"error": "Etapa no encontrada"}, status=404)

        prog, _ = ProgresoEstudiante.objects.get_or_create(
            estudiante=request.user, etapa=etapa
        )
        prog.completada = True
        prog.fecha_completado = date.today()
        prog.save()

        return Response({"mensaje": f"Etapa '{etapa.nombre}' completada ✅"})

    @action(detail=True, methods=['post'], url_path='cargar-estudiantes')
    def cargar_estudiantes_excel(self, request, pk=None):

        laboratorio = self.get_object()
        archivo = request.FILES.get('file')

        if not archivo:
            return Response({"error": "No se envió archivo"}, status=400)

        try:
            df = pd.read_excel(archivo)
        except:
            return Response({"error": "Archivo inválido"}, status=400)

        creados = 0
        errores = []

        with transaction.atomic():
            for index, row in df.iterrows():

                try:
                    usuario = Users.objects.get(correo=row['correo'])

                    if usuario.rol != "estudiante":
                        errores.append(f"Fila {index}: el usuario no es estudiante")
                        continue

                    inscripcion, created = Inscripcion.objects.get_or_create(
                        usuario=usuario,
                        laboratorio=laboratorio,
                        defaults={"fecha_inscripcion": date.today()}
                    )

                    if created:
                        creados += 1
                    else:
                        errores.append(f"Fila {index}: ya inscrito")

                except Users.DoesNotExist:
                    errores.append(f"Fila {index}: usuario no existe")

        return Response({
            "mensaje": "Inscripción finalizada",
            "creados": creados,
            "errores": errores
        })
# =========================================================
# LABORATORIOS PROFESOR
# =========================================================
class MisLaboratoriosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user

        laboratorios = LaboratorioProfesor.objects.filter(
            profesor=usuario
        ).order_by('-fecha_actualizacion')

        serializer = LaboratorioProfesorSerializer(
            laboratorios,
            many=True
        )

        return Response(serializer.data)
    

# =========================================================
# INSCRIBIR USUARIO POR CODIGO
# =========================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def inscribir_usuario(request):

    codigo = request.data.get('codigo_lab')

    try:
        laboratorio = LaboratorioProfesor.objects.get(
            codigo_lab=codigo
        )

    except LaboratorioProfesor.DoesNotExist:

        return Response(
            {"error": "Código inválido"},
            status=404
        )

    # EVITAR INSCRIPCIONES DUPLICADAS
    existe = Inscripcion.objects.filter(
        usuario=request.user,
        laboratorio=laboratorio
    ).exists()

    if existe:

        return Response(
            {"error": "Ya estás inscrito en este laboratorio"},
            status=400
        )

    inscripcion = Inscripcion.objects.create(
        usuario=request.user,
        laboratorio=laboratorio,
        fecha_inscripcion=date.today()
    )

    serializer = InscripcionSerializer(inscripcion)

    return Response(serializer.data, status=201)


# =========================================================
# GENERAR CONTENIDO CON IA
# =========================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generar_contenido_ia(request):
    try:
        campo = request.data.get("campo")
        categoria = request.data.get("categoria")
        objetivo = request.data.get("objetivo")
        palabras_clave = request.data.get("palabras_clave")
        titulo = request.data.get("titulo", "")

        ia = requests.post(
            "https://agentes-ia-9heysq.fly.dev/generar-contenido",
            json={
                
                "categoria": categoria,
                "objetivo": objetivo,
                "palabras_clave": palabras_clave,
                "titulo":titulo
            },
            timeout=30
        ).json()

        return Response({
            "campo": campo,
            "contenido": ia.get(campo, "")
        })
    except:
        return Response({"error": "No se pudo conectar con la IA"}, status=500)
    


