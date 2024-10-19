

from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Ensure that the user is not given superuser or staff privileges
            user.is_superuser = False
            user.is_staff = False
            user.save()
            login(request, user)
            return redirect('home')  # Change 'home' to your desired redirect URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# Simple Login Form
class LoginForm(forms.Form):
    username = forms.CharField(label="Email, Username, or Contact #")
    password = forms.CharField(widget=forms.PasswordInput)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Find user by email, username, or contact number
            try:
                user = CustomUser.objects.get(
                    Q(email=username_or_email) |
                    Q(username=username_or_email) |
                    Q(contact_number=username_or_email)
                )
            except CustomUser.DoesNotExist:
                user = None

            if user is not None and user.check_password(password):  # Check password manually
                login(request, user)
                return redirect('home_view')  # Redirect to home or desired page
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
# Create your views here.
def home_view(request):
    return render(request, 'home.html')