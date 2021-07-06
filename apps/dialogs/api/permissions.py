from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, message):
        if request.method in permissions.SAFE_METHODS:
            return True
        return message.sender == request.user


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user in thread.participants.all()
