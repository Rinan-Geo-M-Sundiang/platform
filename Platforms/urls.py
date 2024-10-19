from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('', login_view, name='login_view'),
    path('home/', home_view, name='home_view'),
    path('create_post/', create_post, name='create_post')
]
