# accounts/forms.py
"""
GRODIUR - ACCOUNTS FORM MODULE
==============================
This module handles all input forms related to user authentication, registration, 
and user/profile data management. It leverages Django's built-in forms framework 
to ensure secure, validated, and sanitized user inputs.
"""

from django import forms
from django.contrib.auth import get_user_model

# Fetch the active User model defined in Django settings (custom or default)
User = get_user_model()

# Import pre-configured creation and authentication forms from Django's secure auth system
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    """
    CUSTOM USER REGISTRATION FORM
    ----------------------------
    Inherits from Django's secure 'UserCreationForm' which automatically handles:
    1. Input sanitization.
    2. Secure password hashing using PBKDF2.
    3. Creation of a new User instance in the database.
    
    This custom version extends it by adding email, first name, and last name 
    as mandatory fields to meet GRODIUR's professional e-commerce requirements.
    """
    # Explicitly define email and name fields to mark them as required in the UI
    email = forms.EmailField(
        required=True,
        help_text="Provide a valid email address for account confirmation and invoice delivery."
    )
    first_name = forms.CharField(
        max_length=50, 
        required=True,
        help_text="Enter your first name."
    )
    last_name = forms.CharField(
        max_length=50, 
        required=True,
        help_text="Enter your last name."
    )

    class Meta:
        """
        METADATA CONFIGURATION
        ----------------------
        Specifies the model to link with this form and maps the database fields 
        that will be populated during registration.
        """
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def clean_email(self):
        """
        CUSTOM EMAIL UNIQUE VALIDATION
        ------------------------------
        Ensures that two users cannot register using the same email address.
        This provides a crucial logical check to avoid duplicate e-commerce accounts.
        """
        email = self.cleaned_data.get('email')
        # Check database if this email already exists in the User table
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(AuthenticationForm):
    """
    SECURE USER LOGIN FORM
    ----------------------
    Inherits from Django's built-in 'AuthenticationForm' which safely checks 
    user credentials (username + password) against database records.
    It automatically implements CSRF defense and protection against brute-force login attempts.
    """
    # Customize the visual styling of input widgets by adding CSS placeholders
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}
    ))


class UserUpdateForm(forms.ModelForm):
    """
    USER DETAIL UPDATE FORM
    -----------------------
    Allows logged-in customers to update their primary credentials (First/Last name).
    - Email and Username are disabled from updates here as they act as 
      unique, secure authentication identifiers across the platform.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    """
    USER PROFILE DETAILS FORM
    -------------------------
    Integrates with the 1-to-1 UserProfile database model, enabling customers to
    manage their phone numbers, delivery addresses, default cities, and profile pictures.
    """
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'profile_picture']