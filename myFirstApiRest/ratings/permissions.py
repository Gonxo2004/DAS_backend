from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Sólo el owner (usuario que creó) puede editar o borrar.
    Otros sólo pueden leer.
    """
    def has_object_permission(self, request, view, obj):
        # Lectura permitida a todos
        if request.method in permissions.SAFE_METHODS:
            return True
        # Escritura sólo al propietario
        return obj.user == request.user