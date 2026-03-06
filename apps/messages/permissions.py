from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission : only author can remove/change message
    Read - all user in channel
    """

    def has_object_permission(self, request, view, obj):
        # Read available all user in channnel
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # only author can remove/change message
        return obj.author == request.user