
from django.contrib.auth.backends import RemoteUserBackend

class RemoteUserWithEmailBackend(RemoteUserBackend):
    domain = 'bu.edu'
    def configure_user(self, user):
        user.email = "{0}@{1}".format(user.username, self.domain)
        user.save()
        return user

