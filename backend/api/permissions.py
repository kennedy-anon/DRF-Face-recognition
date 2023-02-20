from rest_framework.permissions import BasePermission


# permission to perform a face search
class IsCrimeOfficerPermission(BasePermission):
    message = 'You do not have permission to perform a face search.'

    def has_permission(self, request, view):
        # check if the user belongs to the crime officer group
        return request.user.groups.filter(name='CrimeOfficer').exists()


# permission to train the model
class IsSystemAdminPermission(BasePermission):
    message = 'You do not have permission to train the Model.'

    def has_permission(self, request, view):
        # check if the user belongs to the system admin group
        return request.user.groups.filter(name='SystemAdmin').exists()


# permission to view face search logs
class IsSeniorOfficerPermission(BasePermission):
    message = 'You do not have permission to view the Face Search Logs.'

    def has_permission(self, request, view):
        # check if the officer belongs to the senior officer group
        return request.user.groups.filter(name='SeniorOfficer').exists()