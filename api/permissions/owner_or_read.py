from rest_framework import permissions

from flat.models import Flat, Renting
from community.models import Rating


class OwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Flat):
            return bool(request.method in permissions.SAFE_METHODS or request.user == obj.owner)
        if isinstance(obj, Renting):
            return bool(request.method in permissions.SAFE_METHODS or request.user == obj.user)
        if isinstance(obj, Rating):
            return bool(request.method in permissions.SAFE_METHODS or request.user == obj.user)
