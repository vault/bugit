from models import Message
from django import forms

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('sender', 'sent')

