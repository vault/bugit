
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from common.models import Repository, Collaboration

slug_errors = {
        'invalid' : "Use only letters, numbers, underscores, and hyphens",
}

class NewRepositoryForm(forms.Form):
    repo_name = forms.SlugField(max_length=100, error_messages=slug_errors)


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['description', 'long_description', 'is_public']


CollaborationFormSet = inlineformset_factory(Repository, Repository.collaborators.through, exclude=('repository'))
