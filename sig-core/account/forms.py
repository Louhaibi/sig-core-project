from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.widgets import Input
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.db import models


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
    ))


class CreateUserForm(UserCreationForm):

    email = forms.EmailField
    password1 = forms.CharField(widget=forms.TextInput(attrs={
                                    "type": "password",
                                    "class": "form-input",
                                    "id": "password",
                                    "placeholder": "Password"
                                }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
                                    "type": "password",
                                    "class": "form-input",
                                    "id": "re-password",
                                    "placeholder": "Repeat Your Password"
                                }))


    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": Input(attrs={
                "type": "text",
                "class": "form-input",
                "name": "name",
                "id": "name",
                "placeholder": "Username"
            }),
            "email": Input(attrs={
                "type": "email",
                "class": "form-input",
                "name": "email",
                "id": "email",
                "required": True,
                "placeholder": "Email"
            }),

        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()


    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            "username": Input(attrs={

                "type": "text",
                "class": "field",
                "placeholder": "Username",
                "required": True
            }),
            "email": Input(attrs={

                "type": "text",
                "class": "field",
                "required": True,
                "placeholder": "Email"
            }),

        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']




