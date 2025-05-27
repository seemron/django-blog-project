from django import forms
from .models import AccessRequest

class AccessRequestForm(forms.ModelForm):
    class Meta:
        model = AccessRequest
        fields = ['email']
