from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    Permite editar/eliminar una subasta solo si el usuario es el propietario
    o es administrador. Cualquiera puede consultar (GET).
    """
    def has_object_permission(self, request, view, obj):
        # Permitir acceso de lectura a cualquier usuario (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Permitir si el usuario es el creador o es administrador
        return obj.auctioneer == request.user or request.user.is_staff


class IsBidderOrAdmin(BasePermission):
    """
    Permite acceder a la puja si el usuario es el creador (bidder) o es admin.
    Cualquiera puede consultar (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # Lectura pública permitida a todos
        if request.method in SAFE_METHODS:
            return True
        # Solo puede modificar/eliminar si es el creador o admin
        return obj.bidder == request.user or request.user.is_staff