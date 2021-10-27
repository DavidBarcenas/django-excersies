from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from accounts.models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=50,
        error_messages={
            'invalid': 'Entered a valid email.'
        }
    )

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )

        return user

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        emailExists = User.objects.filter(email=email)

        if emailExists.count():
            raise ValidationError('This email already exists!.')

        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'user')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].required = False
