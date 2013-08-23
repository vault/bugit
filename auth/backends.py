
from django.contrib.auth.backends import RemoteUserBackend
from django.conf import settings

class RemoteUserWithEmailBackend(RemoteUserBackend):
    domain = settings.DOMAIN
    def configure_user(self, user):
        user.email = "{0}@{1}".format(user.username, self.domain)
        user.save()
        return user

