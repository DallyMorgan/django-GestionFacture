from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from simple_history import register
from simple_history.admin import SimpleHistoryAdmin





register(CustomUser)

class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'avatar', 'is_staff']

    search_fields = ['username', 'email']

    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']

    list_editable = ['is_staff']

    fieldsets = (
        ('Information de connexion', {'fields': ('username', 'password')}),
        ('Informations Personelles', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
