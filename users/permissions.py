from rest_framework.permissions import BasePermission
from parametros.utils.helpers import get_parametro


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.rol == get_parametro("ROLE_ADMIN")
    
class IsProfesor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.rol == get_parametro("ROLE_PROFESOR")
    

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.rol == get_parametro("ROLE_SUPERADMIN")
    

class IsEstudiante(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.rol == get_parametro("ROLE_ESTUDIANTE")