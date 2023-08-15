from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileSignupForm(forms.ModelForm):
    user_bio = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'maxlength': '200'}))

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
