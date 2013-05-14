
from django import forms
from django.forms import ModelForm, Form

from git.models import *


class PublicKeyForm(ModelForm):
    class Meta:
        model = PublicKey
        fields = ['description', 'pubkey']


class NewRepositoryForm(Form):
    repo_name = forms.SlugField(max_length=100)


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['description', 'long_description', 'is_public', 'collaborators']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

