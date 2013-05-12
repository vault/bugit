
from django.forms import ModelForm

from git.models import *

class PublicKeyForm(ModelForm):
    class Meta:
        model = PublicKey
        fields = ['description', 'pubkey']


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['description', 'is_public', 'collaborators']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


