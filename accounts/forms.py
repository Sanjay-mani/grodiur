# accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ))


class UserUpdateForm(forms.ModelForm):
    """Only allows editing first name and last name.
    Email and username are authentication identifiers and must NOT be editable."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'profile_picture']