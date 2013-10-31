
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
        fields = ['description', 'is_public', 'email_on_update']


class CollaborationForm(ModelForm):
    user = forms.CharField()

    class Meta:
        model = Collaboration
        exclude = ('repository', 'user')

    def __init__(self, **kwargs):
        super(CollaborationForm, self).__init__(**kwargs)
        if 'instance' in kwargs:
            self.fields['user'] = forms.CharField(initial=kwargs['instance'].user.username)

    def clean(self):
        cleaned_data = super(CollaborationForm, self).clean()
        self.instance.full_clean()
        return cleaned_data

    def clean_user(self):
        username = self.cleaned_data['user']
        user = None
        try:
            user = User.objects.get(username=username)
            self.instance.user = user
        except User.DoesNotExist:
            raise forms.ValidationError("User %(username_s does not exist",
                    params={'username':username})



CollaborationFormSet = inlineformset_factory(Repository, Repository.collaborators.through, form=CollaborationForm)

