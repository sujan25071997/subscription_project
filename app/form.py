from django import forms
from app.models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class UserProfileForm(forms.ModelForm):

    class Meta():
        model = UserProfile
        fields = ('email','password')

class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
      model = UserProfile
      fields = ['email', 'name', 'password']
