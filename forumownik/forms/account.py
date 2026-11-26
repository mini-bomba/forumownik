from django import forms
from turnstile.fields import TurnstileField


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = TurnstileField()
