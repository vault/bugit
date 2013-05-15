from django import forms
from django.forms import ModelForm

from common.models import User, PublicKey

class PublicKeyForm(ModelForm):
    class Meta:
        model = PublicKey
        fields = ['description', 'pubkey']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

