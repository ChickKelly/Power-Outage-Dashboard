from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User
import re
from .models import Community 

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        help_text="We'll never share your email with anyone else."
    )
    
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES, 
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Select your role in the power outage response team."
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
        
        # Custom help texts
        self.fields['username'].help_text = "Username must be unique and contain only letters, numbers, and @/./+/-/_ characters."
        self.fields['password1'].help_text = "Password must be at least 8 characters long and contain a mix of letters and numbers."

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError("Please enter a valid email address.")
        
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        
        # Check for inappropriate characters
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and @/./+/-/_ characters.")
        
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise ValidationError("First name can only contain letters and spaces.")
        return first_name.title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-Z\s]+$', last_name):
            raise ValidationError("Last name can only contain letters and spaces.")
        return last_name.title()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("The two password fields didn't match.")
            
            # Additional password strength validation
            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            
            if password1.isdigit():
                raise ValidationError("Password cannot be entirely numeric.")
            
            if not any(c.isalpha() for c in password1):
                raise ValidationError("Password must contain at least one letter.")
        
        return password2

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    
    error_messages = {
        'invalid_login': "Please enter a correct username and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive. Please contact an administrator.",
    }
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            if self.user_cache is None:
                # Check if user exists but password is wrong
                try:
                    user = User.objects.get(username=username)
                    raise ValidationError(
                        "Invalid password. Please check your password and try again.",
                        code='invalid_password'
                    )
                except User.DoesNotExist:
                    raise ValidationError(
                        "Username not found. Please check your username or sign up for a new account.",
                        code='invalid_username'
                    )
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data
class AddCityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'latitude', 'longitude', 'power_status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'power_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }