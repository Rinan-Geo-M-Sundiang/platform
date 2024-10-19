from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post



class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'contact_number']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind?"}),
        max_length=500,  # Limit content length to 500 characters (or any desired length)
        label=''
    )

    class Meta:
        model = Post
        fields = ['content']
