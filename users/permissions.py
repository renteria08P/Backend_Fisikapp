from rest_framework.permissions import BasePermission
from parametros.utils.helpers import get_parametro


def get_roles():
    return {
        "admin": get_parametro("ROLE_ADMIN"),
        "profesor": get_parametro("ROLE_PROFESOR"),
        "estudiante": get_parametro("ROLE_ESTUDIANTE"),
        "superadmin": get_parametro("ROLE_SUPERADMIN"),
    }


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        roles = get_roles()
        return request.user.is_authenticated and request.user.rol == roles["superadmin"]


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        roles = get_roles()
        return request.user.is_authenticated and request.user.rol == roles["admin"]


class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        roles = get_roles()
        return (
            request.user.is_authenticated and
            request.user.rol in [
                roles["admin"],
                roles["superadmin"]
            ]
        )


class IsProfesor(BasePermission):
    def has_permission(self, request, view):
        roles = get_roles()
        return request.user.is_authenticated and request.user.rol == roles["profesor"]