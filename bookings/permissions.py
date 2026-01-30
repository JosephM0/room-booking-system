from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsEditor(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        return user.groups.filter(name='editors').exists() or user.is_superuser

class IsEditorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        return user.groups.filter(name='editors').exists() or user.is_superuser
    
class IsReceptionistOrMarketing(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS:
            return(
                user.groups.filter(name__in=["Marketing", "Receptionist"]).exists() or user.is_superuser
            )
        
        return (
            user.groups.filter(name="Receptionist").exists() or user.is_superuser
        )