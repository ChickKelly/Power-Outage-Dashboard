# outages/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Community

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'role', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    pass

class AddCityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'latitude', 'longitude']
from django import forms
from .models import Community

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = '__all__'  # or a list of specific fields
