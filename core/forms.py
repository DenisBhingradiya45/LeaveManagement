from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class OTPVerificationForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    otp = forms.IntegerField()

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
