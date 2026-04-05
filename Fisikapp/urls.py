"""
URL configuration for Fisikapp project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Routers de develop
from laboratorios.api.router import (
    router_laboratorios,
    router_categorias,
    router_palabras,
    router_objetivos
)

from informes import routers


schema_view = get_schema_view(
   openapi.Info(
      title="API Fisikapp",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("api-auth/", include("rest_framework.urls")),

    # TU APP (inscripciones) ✅
    path('api/', include('inscripciones.urls')),

    # Rutas de develop ✅
    path('informes/', include(routers.router_informes.urls)),
    path('resultados/', include(routers.router_resultados.urls)),
    path('laboratorios/', include(router_laboratorios.urls)),
    path('categorias/', include(router_categorias.urls)),
    path('palabras-clave/', include(router_palabras.urls)),
    path('objetivos/', include(router_objetivos.urls)),
]
