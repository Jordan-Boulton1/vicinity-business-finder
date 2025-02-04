from rest_framework import permissions

class IsReviewOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owners of a review to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
