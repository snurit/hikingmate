from django import forms
from django.forms import ModelForm, forms
from findamate.models import Hike
from django.contrib.auth.forms import UserCreationForm
from findamate.models import User

# Hike form
class HikeForm(ModelForm):
    class Meta:
        model = Hike
        exclude = ['enrolled_hikers']

# Signup form
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
