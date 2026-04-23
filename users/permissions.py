from rest_framework.permissions import BasePermission


class Roles:
    ADMIN = "admin"
    PROFESOR = "profesor"
    ESTUDIANTE = "estudiante"
    SUPERADMIN = "superadmin"


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.rol == Roles.SUPERADMIN
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.rol == Roles.ADMIN
        )


class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.rol in [
                Roles.ADMIN,
                Roles.SUPERADMIN
            ]
        )


class IsProfesor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.rol == Roles.PROFESOR
        )