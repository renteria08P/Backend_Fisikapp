"""
URL configuration for Fisikapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from informes.routers import router as informes_router
from notificaciones.routers import router
from django.http import HttpResponse
from laboratorios.api.router import (
    router_laboratorios,
    router_categorias,
    router_palabras,
    router_objetivos
)

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



def home(request): 
    return HttpResponse("Backend funcionando 🚀")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    # Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("api-auth/", include("rest_framework.urls")),

    # TUS APPS
    path('api/', include('inscripciones.urls')),
    path('api/contenido/', include('contenido.urls')),

    #  INFORMES
    path('api/', include(router.urls)),

    # LABORATORIOS
    path('api/', include(router_laboratorios.urls)),
    path('api/', include(router_categorias.urls)),
    path('api/', include(router_palabras.urls)),
    path('api/', include(router_objetivos.urls)),

    # USERS
    path('api/users/', include('users.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)