from rest_framework import exceptions
from rest_framework.permissions import BasePermission


class ViewPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            slug = view.kwargs.get('slug', None)
            return request.user.queries.filter(slug=slug).exists()
        except exceptions.AuthenticationFailed:
            return False