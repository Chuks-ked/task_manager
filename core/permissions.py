# core/permissions.py
from rest_framework import permissions

class IsAssigneeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the assignee
        return obj.assignee == request.user