from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only methods for everyone
        if request.method in SAFE_METHODS:
            return True

        # Write permissions only for the owner
        return obj.user == request.user
