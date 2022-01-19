from rest_framework import permissions

from flat.models import Flat, Renting
from community.models import Rating


class OwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Flat):
            #Возможность редактировать Flat только собственнику
            return bool(request.method in permissions.SAFE_METHODS or request.user == obj.owner)
        if isinstance(obj, Renting):
            #Возможность редактировать Renting только собственнику
            return bool(request.method in permissions.SAFE_METHODS or request.user == obj.user)
        if isinstance(obj, Rating):
            #Возможность редактировать Rating только собственнику
            return bool(request.method in permissions.SAFE_METHODS or request.user == obj.user)
