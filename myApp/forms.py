from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}

class donateForm(UserChangeForm):
    password = None
    amount = forms.IntegerField(label='Amount')
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'amount']
        labels = {'email': 'Email'}        