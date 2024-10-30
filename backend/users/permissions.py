from rest_framework import permissions
    

class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'user' in request.user.groups.values_list("name", flat=True):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if 'user' in request.user.groups.values_list("name", flat=True):
            return True
        return False