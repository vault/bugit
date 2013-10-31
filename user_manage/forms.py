
from django import forms
from django.forms import ModelForm

from common.models import User, PublicKey, UserProfile

slug_errors = {
        'invalid' : "Use only letters, numbers, underscores, and hyphens",
}

class PublicKeyForm(ModelForm):
    description = forms.SlugField(max_length=100, error_messages=slug_errors)
    pubkey = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = PublicKey
        fields = ['description', 'pubkey']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['never_email']
