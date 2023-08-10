from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

#create profile here by overriding save method.


class ProfileSignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_bio']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_bio', 'user_dp']


