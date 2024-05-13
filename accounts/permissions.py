from rest_framework.permissions import BasePermission

from accounts.models import CustomerUser, BrndAdmin


class IsCustomerUser(BasePermission):
    """
    Allows access only to authenticated users who are brand admins.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and CustomerUser.objects.filter(user=request.user).exists()


class IsAdminBrandAdmin(BasePermission):
    """
    Allows access only to authenticated users who are customers.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and BrndAdmin.objects.filter(user=request.user).exists()
