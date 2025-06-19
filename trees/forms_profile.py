from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Old password')
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=True, label='New password')
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirm password')
