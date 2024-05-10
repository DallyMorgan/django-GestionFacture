from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from simple_history import register
from simple_history.admin import SimpleHistoryAdmin





register(CustomUser)

class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):
    # Liste des attributs à afficher dans la liste des utilisateurs
    list_display = ['username', 'email', 'first_name', 'last_name', 'avatar', 'is_staff']

    # Champs de recherche pour le panneau d'administration
    search_fields = ['username', 'email']

    # Champs pour filtrer les utilisateurs dans le panneau d'administration
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']

    # Champs éditables dans la liste des utilisateurs
    list_editable = ['is_staff']

    # Champs du formulaire d'ajout d'un utilisateur
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(CustomUser, SimpleHistoryAdmin)
