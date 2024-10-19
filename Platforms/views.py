

from .forms import *

from django.contrib.auth import authenticate, login

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm

from .models import Post, CustomUser
def format_username(username):
    if len(username) <= 3:
        return username  # Handle short usernames
    elif len(username) <= 5:
        # For usernames of length 4 or 5, show first 2 chars and last 1 char
        return f"{username[:2]}***{username[-1:]}"
    else:
        # For usernames longer than 5, show first 2 and last 3 chars
        return f"{username[:2]}***{username[-3:]}"

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = False
            user.is_staff = False
            user.is_active = False  # User cannot log in until approved
            user.save()
            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('login_view')
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
    posts = Post.objects.all()

    # Format username and truncate content
    formatted_posts = []
    for post in posts:
        truncated = False
        if len(post.content) > 100:
            truncated = True
            truncated_content = post.content[:100] + '...'
        else:
            truncated_content = post.content

        formatted_posts.append({
            'username': format_username(post.user.username),
            'content': truncated_content,
            'original_content': post.content,
            'truncated': truncated,
            'created_at': post.created_at.strftime('%Y-%m-%d'),
            'post_id': post.id,
        })
    return render(request, 'home.html', {'posts': formatted_posts})


def create_post(request):
    user = request.user

    # Check if the user has already posted
    if Post.objects.filter(user=user).exists():
        messages.error(request, "You can only post once.")
        return redirect('home_view')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user  # Assign the current user to the post
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('home_view')
        else:
            messages.error(request, "There was an error in your submission.")
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})