"""
User Forms Module
These forms are associated with the 'users' app in the Django project.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserLoginForm(forms.ModelForm):
    """
    A form for user login.
    """
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the form.
        """
        model = User
        fields = ['email', 'password']


# pylint: disable=too-many-ancestors
class UserSignupForm(UserCreationForm):
    """
    A form for user signup, extending the UserCreationForm.
    """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the form.
        """
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        """
        Validate that the provided email is not already in use.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use."
                                        " Please use a different email.")
        return email

    def save(self, commit=True):
        """
        Save the user object with the provided password and email.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileSignupForm(forms.ModelForm):
    """
    A form for profile signup.
    """
    user_bio = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'maxlength': '200'}))

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the form.
        """
        model = Profile
        fields = ['user_bio']


class UserEditForm(forms.ModelForm):
    """
    A form for editing user information.
    """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the form.
        """
        model = User
        fields = ['first_name', 'last_name']


class ProfileEditForm(forms.ModelForm):
    """
    A form for editing user profile information.
    """
    user_bio = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'maxlength': '200'}))

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the form.
        """
        model = Profile
        fields = ['user_bio']
