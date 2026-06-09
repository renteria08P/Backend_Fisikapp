from django.shortcuts import render

from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import (
    ConceptosBasicos,
    Practica,
    Procedimiento,
    Formula,
    Bibliografia,
    Recursos
)
from .serializers import (
    ConceptosBasicosSerializer,
    PracticaSerializer,
    ProcedimientoSerializer,
    FormulaSerializer,
    BibliografiaSerializer, 
    RecursosSerializer
)

from .serializers import (
    ConceptosBasicosSerializer,
    PracticaSerializer,
    ProcedimientoSerializer,
    FormulaSerializer,
    BibliografiaSerializer,
    RecursosSerializer,

    PlantillaPracticaSerializer,
    PlantillaProcedimientoSerializer,
    PlantillaFormulaSerializer,
    PlantillaBibliografiaSerializer
)
from .models import (
    ConceptosBasicos,
    Practica,
    Procedimiento,
    Formula,
    Bibliografia,
    Recursos,

    PlantillaPractica,
    PlantillaProcedimiento,
    PlantillaFormula,
    PlantillaBibliografia
)
# =========================
# CONCEPTOS BASICOS
# =========================

@swagger_auto_schema(method='post', request_body=ConceptosBasicosSerializer)
@api_view(['GET', 'POST'])
def conceptos_list(request):
    if request.method == 'GET':
        data = ConceptosBasicos.objects.all()
        serializer = ConceptosBasicosSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ConceptosBasicosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@swagger_auto_schema(method='put', request_body=ConceptosBasicosSerializer)
@api_view(['PUT', 'DELETE'])
def conceptos_detalle(request, pk):
    try:
        obj = ConceptosBasicos.objects.get(pk=pk)
    except ConceptosBasicos.DoesNotExist:
        return Response({"error": "No existe"}, status=404)

    if request.method == 'PUT':
        serializer = ConceptosBasicosSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return Response({"mensaje": "Eliminado"}, status=204)

# =========================
# PRACTICAS
# =========================

@swagger_auto_schema(method='post', request_body=PracticaSerializer)
@api_view(['GET', 'POST'])
def practicas_list(request):
    if request.method == 'GET':
        laboratorio_id = request.query_params.get('laboratorio', None)     # ← NUEVO
        data = Practica.objects.all()
        if laboratorio_id:                                               # ← NUEVO
            data = data.filter(laboratorio=laboratorio_id)                # ← NUEVO
        serializer = PracticaSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PracticaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@swagger_auto_schema(method='put', request_body=PracticaSerializer)
@api_view(['PUT', 'DELETE'])
def practicas_detalle(request, pk):
    try:
        obj = Practica.objects.get(pk=pk)
    except Practica.DoesNotExist:
        return Response({"error": "No existe"}, status=404)

    if request.method == 'PUT':
        serializer = PracticaSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return Response({"mensaje": "Eliminado"}, status=204)

# =========================
# PROCEDIMIENTOS
# =========================

@swagger_auto_schema(method='post', request_body=ProcedimientoSerializer)
@api_view(['GET', 'POST'])
def procedimientos_list(request):
    if request.method == 'GET':
        laboratorio_id = request.query_params.get('laboratorio', None)
        data = Procedimiento.objects.all()
        if laboratorio_id:                                               # ← NUEVO
            data = data.filter(laboratorio=laboratorio_id) 
        serializer = ProcedimientoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProcedimientoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@swagger_auto_schema(method='put', request_body=ProcedimientoSerializer)
@api_view(['PUT', 'DELETE'])
def procedimientos_detalle(request, pk):
    try:
        obj = Procedimiento.objects.get(pk=pk)
    except Procedimiento.DoesNotExist:
        return Response({"error": "No existe"}, status=404)

    if request.method == 'PUT':
        serializer = ProcedimientoSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return Response({"mensaje": "Eliminado"}, status=204)
    
# =========================
# FORMULAS
# =========================

@swagger_auto_schema(method='post', request_body=FormulaSerializer)
@api_view(['GET', 'POST'])
def lista_formulas(request):
    if request.method == 'GET':
        laboratorio_id = request.query_params.get('laboratorio', None)  # ← NUEVO
        formulas = Formula.objects.all()
        if laboratorio_id:                                               # ← NUEVO
            formulas = formulas.filter(laboratorio=laboratorio_id)        # ← NUEVO
        serializer = FormulaSerializer(formulas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FormulaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@swagger_auto_schema(method='put', request_body=FormulaSerializer)
@swagger_auto_schema(method='patch', request_body=FormulaSerializer)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def detalle_formula(request, pk):
    try:
        formula = Formula.objects.get(pk=pk)
    except Formula.DoesNotExist:
        return Response({"error": "No encontrado"}, status=404)

    if request.method == 'GET':
        serializer = FormulaSerializer(formula)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FormulaSerializer(formula, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':
        serializer = FormulaSerializer(formula, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        formula.delete()
        return Response({"mensaje": "Eliminado correctamente"}, status=204)


# =========================
# BIBLIOGRAFIA
# =========================

@swagger_auto_schema(method='post', request_body=BibliografiaSerializer)
@api_view(['GET', 'POST'])
def lista_bibliografia(request):
    if request.method == 'GET':
        laboratorio_id = request.query_params.get('laboratorio', None)  # ← NUEVO
        biblios = Bibliografia.objects.all()
        if laboratorio_id:                                               # ← NUEVO
            biblios = biblios.filter(laboratorio=laboratorio_id)          # ← NUEVO
        serializer = BibliografiaSerializer(biblios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BibliografiaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@swagger_auto_schema(method='put', request_body=BibliografiaSerializer)
@swagger_auto_schema(method='patch', request_body=BibliografiaSerializer)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def detalle_bibliografia(request, pk):
    try:
        biblio = Bibliografia.objects.get(pk=pk)
    except Bibliografia.DoesNotExist:
        return Response({"error": "No encontrado"}, status=404)

    if request.method == 'GET':
        serializer = BibliografiaSerializer(biblio)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BibliografiaSerializer(biblio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':
        serializer = BibliografiaSerializer(biblio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        biblio.delete()
        return Response({"mensaje": "Eliminado correctamente"}, status=204)


# =========================
# RECURSOS
# =========================

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Recursos
from .serializers import RecursosSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def recursos_list(request):
    if request.method == 'GET':
        recursos = Recursos.objects.all()
        serializer = RecursosSerializer(recursos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecursosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def recursos_detalle(request, pk):
    try:
        recurso = Recursos.objects.get(pk=pk)
    except Recursos.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = RecursosSerializer(recurso)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RecursosSerializer(recurso, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        recurso.delete()
        return Response(status=204)
    

# =========================================================
# PLANTILLA PRACTICA
# =========================================================
class PlantillaPracticaViewSet(ModelViewSet):

    queryset = PlantillaPractica.objects.all()
    serializer_class = PlantillaPracticaSerializer
    permission_classes = [IsAuthenticated]


# =========================================================
# PLANTILLA PROCEDIMIENTO
# =========================================================
class PlantillaProcedimientoViewSet(ModelViewSet):

    queryset = PlantillaProcedimiento.objects.all()
    serializer_class = PlantillaProcedimientoSerializer
    permission_classes = [IsAuthenticated]


# =========================================================
# PLANTILLA FORMULA
# =========================================================
class PlantillaFormulaViewSet(ModelViewSet):

    queryset = PlantillaFormula.objects.all()
    serializer_class = PlantillaFormulaSerializer
    permission_classes = [IsAuthenticated]


# =========================================================
# PLANTILLA BIBLIOGRAFIA
# =========================================================
class PlantillaBibliografiaViewSet(ModelViewSet):

    queryset = PlantillaBibliografia.objects.all()
    serializer_class = PlantillaBibliografiaSerializer
    permission_classes = [IsAuthenticated]