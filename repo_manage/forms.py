
from django import forms
from django.forms import ModelForm, Form

from common.models import Repository


class NewRepositoryForm(Form):
    repo_name = forms.SlugField(max_length=100)


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['description', 'long_description', 'is_public', 'collaborators']


