from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'contact_number', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'contact_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)

