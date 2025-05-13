from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Sólo el owner (usuario que creó) puede editar o borrar.
    Otros sólo pueden leer.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user