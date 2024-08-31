from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'password'}))

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': '<PASSWORD>'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password']!= cd['password2']:
            return cd['password2']
        else:
            raise forms.ValidationError("Passwords don't match")