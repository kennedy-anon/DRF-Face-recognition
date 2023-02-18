from rest_framework.permissions import BasePermission


# permission to perform a face search
class IsCrimeOfficerPermission(BasePermission):
    def has_permission(self, request, view):
        # check if the user belongs to the crime officer group
        return request.user.groups.filter(name='CrimeOfficer').exists()


# permission to train the model
class IsSystemAdminPermission(BasePermission):
    def has_permission(self, request, view):
        # check if the user belongs to the system admin group
        return request.user.groups.filter(name='SystemAdmin').exists()
