from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from drf_yasg.utils import swagger_auto_schema

from .models import ConceptosBasicos, Practicas, Procedimientos, Formulas, Bibliografia, Recursos
from .serializers import (
    ConceptosBasicosSerializer,
    PracticasSerializer,
    ProcedimientosSerializer,
    FormulasSerializer,
    BibliografiaSerializer, 
    RecursosSerializer
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser


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

@swagger_auto_schema(method='post', request_body=PracticasSerializer)
@api_view(['GET', 'POST'])
def practicas_list(request):
    if request.method == 'GET':
        laboratorio_id = request.query_params.get('laboratorio', None)     # ← NUEVO
        data = Practicas.objects.all()
        if laboratorio_id:                                               # ← NUEVO
            data = data.filter(laboratorio=laboratorio_id)                # ← NUEVO
        serializer = PracticasSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PracticasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@swagger_auto_schema(method='put', request_body=PracticasSerializer)
@api_view(['PUT', 'DELETE'])
def practicas_detalle(request, pk):
    try:
        obj = Practicas.objects.get(pk=pk)
    except Practicas.DoesNotExist:
        return Response({"error": "No existe"}, status=404)

    if request.method == 'PUT':
        serializer = PracticasSerializer(obj, data=request.data)
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

@swagger_auto_schema(method='post', request_body=ProcedimientosSerializer)
@api_view(['GET', 'POST'])
def procedimientos_list(request):
    if request.method == 'GET':
        laboratorio_id = request.query_params.get('laboratorio', None)
        data = Procedimientos.objects.all()
        if laboratorio_id:                                               # ← NUEVO
            data = data.filter(laboratorio=laboratorio_id) 
        serializer = ProcedimientosSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProcedimientosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@swagger_auto_schema(method='put', request_body=ProcedimientosSerializer)
@api_view(['PUT', 'DELETE'])
def procedimientos_detalle(request, pk):
    try:
        obj = Procedimientos.objects.get(pk=pk)
    except Procedimientos.DoesNotExist:
        return Response({"error": "No existe"}, status=404)

    if request.method == 'PUT':
        serializer = ProcedimientosSerializer(obj, data=request.data)
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

@swagger_auto_schema(method='post', request_body=FormulasSerializer)
@api_view(['GET', 'POST'])
def lista_formulas(request):
    if request.method == 'GET':
        laboratorio_id = request.query_params.get('laboratorio', None)  # ← NUEVO
        formulas = Formulas.objects.all()
        if laboratorio_id:                                               # ← NUEVO
            formulas = formulas.filter(laboratorio=laboratorio_id)        # ← NUEVO
        serializer = FormulasSerializer(formulas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FormulasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@swagger_auto_schema(method='put', request_body=FormulasSerializer)
@swagger_auto_schema(method='patch', request_body=FormulasSerializer)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def detalle_formula(request, pk):
    try:
        formula = Formulas.objects.get(pk=pk)
    except Formulas.DoesNotExist:
        return Response({"error": "No encontrado"}, status=404)

    if request.method == 'GET':
        serializer = FormulasSerializer(formula)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FormulasSerializer(formula, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':
        serializer = FormulasSerializer(formula, data=request.data, partial=True)
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