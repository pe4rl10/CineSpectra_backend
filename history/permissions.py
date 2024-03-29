from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of a history object to create/read it.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            # Allow read-only access to history objects
            return True
        elif request.user.is_authenticated:
            # Ensure the user is authenticated for any write operations
            user_id = request.data.get('user')
            return user_id == str(request.user.id)
        return False

    def has_object_permission(self, request, view, obj):
        # Ensure the object has a 'user' attribute and the user is authenticated
        if hasattr(obj, 'user') and request.user.is_authenticated:
            # Allow the owner of the history object to view it
            return obj.user == request.user
        return False
