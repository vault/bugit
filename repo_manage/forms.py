
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from common.models import Repository, Collaboration, User

slug_errors = {
        'invalid' : "Use only letters, numbers, underscores, and hyphens",
}

class NewRepositoryForm(forms.Form):
    repo_name = forms.SlugField(max_length=100, error_messages=slug_errors)


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['description', 'long_description', 'is_public']


class CollaborationForm(ModelForm):
    user = forms.CharField()

    class Meta:
        model = Collaboration
        exclude = ('repository', 'user')

    def __init__(self, **kwargs):
        super(CollaborationForm, self).__init__(**kwargs)
        if 'instance' in kwargs:
            print kwargs['instance']
            self.fields['user'] = forms.CharField(initial=kwargs['instance'].user.username)

    def save(self, **kwargs):
        username = self.cleaned_data['user']
        user = User.objects.get(username=username)
        self.instance.user = user

        return super(CollaborationForm, self).save(**kwargs)




CollaborationFormSet = inlineformset_factory(Repository, Repository.collaborators.through, form=CollaborationForm)

