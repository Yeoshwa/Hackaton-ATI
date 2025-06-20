from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    Permission pour n'autoriser que l'auteur ou un admin à modifier/supprimer.
    """
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée à tous
        if request.method in SAFE_METHODS:
            return True
        # Modification/suppression : auteur ou admin
        return (obj.user == request.user) or request.user.is_staff 