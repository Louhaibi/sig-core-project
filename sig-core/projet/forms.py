from .models import *
from django import forms

class CreateProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = '__all__'
        exclude = ['user']
        communes = forms.ModelMultipleChoiceField(
            required=False,
            queryset=Commune.objects.all(),
            widget=forms.CheckboxSelectMultiple
            )



