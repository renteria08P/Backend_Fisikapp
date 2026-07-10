from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, parser_classes, permission_classes
from users.permissions import (IsAdminSuperAdminOrProfesor)
from rest_framework.response import Response
from .serializers import RecursosSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg import openapi

from .models import (
    ConceptoLaboratorio,
    ConceptosBasicos,
    Practica,
    Procedimiento,
    Formula,
    Recursos,
)

from .serializers import (
    ConceptoLaboratorioSerializer,
    ConceptosBasicosSerializer,
    PracticaSerializer,
    ProcedimientoSerializer,
    FormulaSerializer,
    RecursosSerializer,
    ProcedimientoSwaggerSerializer,
)


# ==============================================
# CONCEPTOS BASICOS
# ==============================================

@swagger_auto_schema(
    method='get',
    operation_summary="Listar conceptos básicos",
    operation_description="""
    Retorna todos los conceptos básicos registrados
    para apoyar el desarrollo de laboratorios.
    """
)
@swagger_auto_schema(
    method='post',
    operation_summary="Crear concepto básico",
    operation_description="""
    Permite registrar un nuevo concepto básico.
    """,
    request_body=ConceptosBasicosSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminSuperAdminOrProfesor])
def conceptos_list(request):

    if request.method == 'GET':

        conceptos = ConceptosBasicos.objects.all()

        serializer = ConceptosBasicosSerializer(
            conceptos,
            many=True
        )

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = ConceptosBasicosSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


@swagger_auto_schema(
    method='put',
    operation_summary="Actualizar concepto básico",
    operation_description="""
    Actualiza la información de un concepto básico existente.
    """,
    request_body=ConceptosBasicosSerializer
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Eliminar concepto básico",
    operation_description="""
    Elimina un concepto básico del sistema.
    """
)
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminSuperAdminOrProfesor])
def conceptos_detalle(request, pk):


    try:

        concepto = ConceptosBasicos.objects.get(
            pk=pk
        )

    except ConceptosBasicos.DoesNotExist:

        return Response(
            {
                "error": "Concepto básico no encontrado"
            },
            status=404
        )

    if request.method == 'PUT':

        serializer = ConceptosBasicosSerializer(
            concepto,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

    elif request.method == 'DELETE':

        concepto.delete()

        return Response(
            {
                "mensaje": "Concepto básico eliminado correctamente"
            },
            status=204
        )
    


# ==============================================
# CONCEPTO LABORATORIO
# ==============================================

@swagger_auto_schema(
    method='get',
    operation_summary="Listar conceptos de un laboratorio",
    operation_description="""
    Retorna los conceptos asociados a un laboratorio,
    incluyendo los recursos agregados por el profesor.
    """
)
@swagger_auto_schema(
    method='post',
    operation_summary="Crear concepto de laboratorio",
    operation_description="""
    Asocia un concepto básico a un laboratorio.
    """,
    request_body=ConceptoLaboratorioSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminSuperAdminOrProfesor])
def conceptos_laboratorio_list(request):

    if request.method == 'GET':

        laboratorio_id = request.query_params.get(
            'laboratorio',
            None
        )

        conceptos = ConceptoLaboratorio.objects.all()

        if laboratorio_id:
            conceptos = conceptos.filter(
                laboratorio=laboratorio_id
            )

        serializer = ConceptoLaboratorioSerializer(
            conceptos,
            many=True
        )

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = ConceptoLaboratorioSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


@swagger_auto_schema(
    method='get',
    operation_summary="Detalle de concepto de laboratorio"
)
@swagger_auto_schema(
    method='put',
    operation_summary="Actualizar concepto de laboratorio",
    request_body=ConceptoLaboratorioSerializer
)
@swagger_auto_schema(
    method='patch',
    operation_summary="Actualizar parcialmente concepto de laboratorio",
    request_body=ConceptoLaboratorioSerializer
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Eliminar concepto de laboratorio"
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminSuperAdminOrProfesor])
def conceptos_laboratorio_detalle(request, pk):

    try:

        concepto = ConceptoLaboratorio.objects.get(
            pk=pk
        )

    except ConceptoLaboratorio.DoesNotExist:

        return Response(
            {
                "error": "Concepto de laboratorio no encontrado"
            },
            status=404
        )

    if request.method == 'GET':

        serializer = ConceptoLaboratorioSerializer(
            concepto
        )

        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:

        serializer = ConceptoLaboratorioSerializer(
            concepto,
            data=request.data,
            partial=request.method == 'PATCH'
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    elif request.method == 'DELETE':

        concepto.delete()

        return Response(
            {
                "mensaje": "Concepto de laboratorio eliminado correctamente"
            },
            status=204
        )

# ==============================================
# PRACTICAS
# ==============================================

@swagger_auto_schema(
    method='get',
    operation_summary="Listar prácticas",
    operation_description="""
    Retorna todas las prácticas registradas.
    Puede filtrarse por laboratorio mediante
    el parámetro ?laboratorio=id.
    """
)
@swagger_auto_schema(
    method='post',
    operation_summary="Crear práctica",
    operation_description="""
    Permite registrar una nueva práctica.
    """,
    request_body=PracticaSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminSuperAdminOrProfesor])
def practicas_list(request):

    if request.method == 'GET':

        laboratorio_id = request.query_params.get(
            'laboratorio',
            None
        )

        practicas = Practica.objects.all()

        if laboratorio_id:
            practicas = practicas.filter(
                laboratorio=laboratorio_id
            )

        serializer = PracticaSerializer(
            practicas,
            many=True
        )

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = PracticaSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


@swagger_auto_schema(
    method='put',
    operation_summary="Actualizar práctica",
    operation_description="""
    Actualiza la información de una práctica.
    """,
    request_body=PracticaSerializer
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Eliminar práctica",
    operation_description="""
    Elimina una práctica registrada.
    """
)
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminSuperAdminOrProfesor])
def practicas_detalle(request, pk):

    try:

        practica = Practica.objects.get(
            pk=pk
        )

    except Practica.DoesNotExist:

        return Response(
            {
                "error": "Práctica no encontrada"
            },
            status=404
        )

    if request.method == 'PUT':

        serializer = PracticaSerializer(
            practica,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

    elif request.method == 'DELETE':

        practica.delete()

        return Response(
            {
                "mensaje": "Práctica eliminada correctamente"
            },
            status=204
        )
        
# ==============================================
# PROCEDIMIENTOS
# ==============================================
@swagger_auto_schema(
    method='get',
    operation_summary="Listar procedimientos",
    operation_description="""
    Retorna todos los procedimientos registrados.
    Puede filtrarse por laboratorio mediante
    el parámetro ?laboratorio=id.
    """
)
@swagger_auto_schema(
    method="post",
    operation_summary="Crear procedimiento",
    operation_description="Permite registrar un nuevo procedimiento.",
    consumes=["multipart/form-data"],
    manual_parameters=[
        openapi.Parameter(
            "laboratorio",
            openapi.IN_FORM,
            description="ID del laboratorio",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
        openapi.Parameter(
            "paso_numero",
            openapi.IN_FORM,
            description="Número del paso",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
        openapi.Parameter(
            "descripcion",
            openapi.IN_FORM,
            description="Descripción del procedimiento",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "orden",
            openapi.IN_FORM,
            description="Orden del procedimiento",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
        openapi.Parameter(
            "imagen",
            openapi.IN_FORM,
            description="Imagen del procedimiento",
            type=openapi.TYPE_FILE,
            required=False,
        ),
    ],
    responses={
        201: ProcedimientoSerializer
    },
)

@api_view(['GET', 'POST'])
@parser_classes([
    MultiPartParser,
    FormParser,
    JSONParser
])
@permission_classes([IsAdminSuperAdminOrProfesor])
def procedimientos_list(request):


    if request.method == 'GET':

        laboratorio_id = request.query_params.get(
            'laboratorio',
            None
        )

        procedimientos = Procedimiento.objects.all()

        if laboratorio_id:
            procedimientos = procedimientos.filter(
                laboratorio=laboratorio_id
            )

        serializer = ProcedimientoSerializer(
            procedimientos,
            many=True
        )

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = ProcedimientoSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


@swagger_auto_schema(
    method='put',
    operation_summary="Actualizar procedimiento",
    operation_description="""
    Actualiza la información de un procedimiento.
    """,
    request_body=ProcedimientoSerializer
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Eliminar procedimiento",
    operation_description="""
    Elimina un procedimiento registrado.
    """
)
@api_view(['PUT', 'PATCH', 'DELETE'])
@parser_classes([
    MultiPartParser,
    FormParser,
    JSONParser
])
@permission_classes([IsAdminSuperAdminOrProfesor])
def procedimientos_detalle(request, pk):

    try:

        procedimiento = Procedimiento.objects.get(
            pk=pk
        )

    except Procedimiento.DoesNotExist:

        return Response(
            {
                "error": "Procedimiento no encontrado"
            },
            status=404
        )

    if request.method == 'PUT':

        serializer = ProcedimientoSerializer(
            procedimiento,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

    elif request.method == 'DELETE':

        procedimiento.delete()

        return Response(
            {
                "mensaje": "Procedimiento eliminado correctamente"
            },
            status=204
        )

# ==============================================
# FORMULAS
# ==============================================

@swagger_auto_schema(
    method='get',
    operation_summary="Listar fórmulas",
    operation_description="""
    Retorna todas las fórmulas registradas.
    Puede filtrarse por laboratorio mediante
    el parámetro ?laboratorio=id.
    """
)
@swagger_auto_schema(
    method='post',
    operation_summary="Crear fórmula",
    operation_description="""
    Permite registrar una nueva fórmula.
    """,
    request_body=FormulaSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminSuperAdminOrProfesor])
def lista_formulas(request):

    if request.method == 'GET':

        laboratorio_id = request.query_params.get(
            'laboratorio',
            None
        )

        formulas = Formula.objects.all()

        if laboratorio_id:
            formulas = formulas.filter(
                laboratorio=laboratorio_id
            )

        serializer = FormulaSerializer(
            formulas,
            many=True
        )

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = FormulaSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


@swagger_auto_schema(
    method='get',
    operation_summary="Detalle de fórmula",
    operation_description="""
    Obtiene la información de una fórmula específica.
    """
)
@swagger_auto_schema(
    method='put',
    operation_summary="Actualizar fórmula",
    operation_description="""
    Actualiza completamente una fórmula.
    """,
    request_body=FormulaSerializer
)
@swagger_auto_schema(
    method='patch',
    operation_summary="Actualizar parcialmente fórmula",
    operation_description="""
    Actualiza uno o varios campos de una fórmula.
    """,
    request_body=FormulaSerializer
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Eliminar fórmula",
    operation_description="""
    Elimina una fórmula registrada.
    """
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminSuperAdminOrProfesor])
def detalle_formula(request, pk):

    try:

        formula = Formula.objects.get(
            pk=pk
        )

    except Formula.DoesNotExist:

        return Response(
            {
                "error": "Fórmula no encontrada"
            },
            status=404
        )

    if request.method == 'GET':

        serializer = FormulaSerializer(
            formula
        )

        return Response(
            serializer.data
        )

    elif request.method == 'PUT':

        serializer = FormulaSerializer(
            formula,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

    elif request.method == 'PATCH':

        serializer = FormulaSerializer(
            formula,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

    elif request.method == 'DELETE':

        formula.delete()

        return Response(
            {
                "mensaje": "Fórmula eliminada correctamente"
            },
            status=204
        )


# ==============================================
# RECURSOS
# ==============================================

@swagger_auto_schema(
    method='get',
    operation_summary="Listar recursos",
    operation_description="""
    Retorna todos los recursos registrados
    en el sistema.
    """
)
@swagger_auto_schema(
    method='post',
    operation_summary="Crear recurso",
    operation_description="""
    Permite registrar un nuevo recurso,
    incluyendo archivos adjuntos.
    """,
    request_body=RecursosSerializer
)
@api_view(['GET', 'POST'])
@parser_classes([
    MultiPartParser,
    FormParser,
    JSONParser
])
@permission_classes([IsAdminSuperAdminOrProfesor])
def recursos_list(request):

    if request.method == 'GET':

        recursos = Recursos.objects.all()

        serializer = RecursosSerializer(
            recursos,
            many=True
        )

        return Response(
            serializer.data
        )

    elif request.method == 'POST':

        serializer = RecursosSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


@swagger_auto_schema(
    method='get',
    operation_summary="Detalle de recurso",
    operation_description="""
    Obtiene la información de un recurso específico.
    """
)
@swagger_auto_schema(
    method='put',
    operation_summary="Actualizar recurso",
    operation_description="""
    Actualiza completamente un recurso.
    """,
    request_body=RecursosSerializer
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Eliminar recurso",
    operation_description="""
    Elimina un recurso registrado.
    """
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminSuperAdminOrProfesor])
@parser_classes([
    MultiPartParser, 
    FormParser,
    JSONParser
])
def recursos_detalle(request, pk):

    try:

        recurso = Recursos.objects.get(
            pk=pk
        )

    except Recursos.DoesNotExist:

        return Response(
            {
                "error": "Recurso no encontrado"
            },
            status=404
        )

    if request.method == 'GET':

        serializer = RecursosSerializer(
            recurso
        )

        return Response(
            serializer.data
        )

    elif request.method == 'PUT':

        serializer = RecursosSerializer(
            recurso,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

    elif request.method == 'DELETE':

        recurso.delete()

        return Response(
            {
                "mensaje": "Recurso eliminado correctamente"
            },
            status=204
        )
    
    elif request.method == 'PATCH':

        serializer = RecursosSerializer(
            recurso,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )
