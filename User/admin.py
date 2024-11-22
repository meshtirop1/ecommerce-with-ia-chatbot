from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Assuming your custom user model is called CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
