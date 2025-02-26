"""
This module provides custom permission classes for the hydroponics application.

It includes:
    - IsOwnerOrReadOnly: A permission class that only allows owners of an object to modify it.
"""

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class IsSelfOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
      - Unauthenticated users to list user profiles (which should only include public fields).
      - Authenticated users to retrieve, update, or delete only their own profile.
    """
    def has_permission(self, request, view):
        # Allow anyone to list users.
        if view.action == 'list':
            return True
        # Disallow user creation via this viewset.
        if view.action == 'create':
            return False
        # For other actions, ensure the user is authenticated.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For detail endpoints (retrieve, update, partial_update, destroy), only allow if the object is the user.
        return obj == request.user