from rest_framework import permissions

class IsStoreOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'store_owner')

class IsStaffAssignedOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Owner can always
        if request.user.role == 'store_owner' and request.user.vendor == obj.vendor:
            return True
        # Staff can only if assigned and same vendor
        if request.user.role == 'staff' and request.user.vendor == obj.vendor:
            # we assume obj has assigned_to field
            return getattr(obj, 'assigned_to', None) == request.user
        return False

class IsVendorObject(permissions.BasePermission):
    """Allow only objects belonging to user's vendor."""
    def has_object_permission(self, request, view, obj):
        vendor = getattr(obj, 'vendor', None)
        return vendor is not None and request.user.vendor == vendor

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'customer'