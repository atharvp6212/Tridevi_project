# users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')
        
class OwnerRegistrationForm(UserCreationForm):
    OWNER_TYPE_CHOICES = [
        ('restaurant_owner', 'Restaurant Owner'),
        ('grocery_owner', 'Grocery Store Owner'),
    ]
    owner_type = forms.ChoiceField(choices=OWNER_TYPE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'owner_type')

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'multiple': False}),
        }
