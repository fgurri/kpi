from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ldap3.core.exceptions import LDAPOperationsErrorResult

class ActiveDirectoryBackend:

    def nautilus_authenticate(username=None, password=None):
        user = None
        try:
            user = authenticate(username=username, password=password)
            # TODO raises LDAPOperationsErrorResult on success login for no reason
            # following code will not be executed
        except LDAPOperationsErrorResult:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user
                user = User(username=username)
                user.save()
        return user
