from django import forms
from .models import Post, Profile

class CreateForm(forms.ModelForm):
      class Meta:
            model = Post
            fields = ['title', 'body']
class CommentForm(forms.Form):
      comment = forms.CharField(required = True, max_length = 600, min_length =3, strip = True)
      
  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User      
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
# Create a UserUpdateForm to update username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Create a ProfileUpdateForm to update image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
      
