from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class AadharVerificationForm(forms.Form):
    number = forms.DecimalField()
    aadhar_id = forms.ImageField()
    captcha = forms.CharField()

class PanVerificationForm(forms.Form):
    pancard = forms.ImageField()

class DrivingVerificationForm(forms.Form):
    driving_license = forms.ImageField()

class OtpForm(forms.Form):
    otp=forms.IntegerField()