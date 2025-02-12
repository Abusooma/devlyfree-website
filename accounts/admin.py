from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    compressed_fields = ['username']
    list_display = ['email', 'username', 'full_name',
                    'date_joined', 'is_active', 'account_status']
    list_display_links = ['email']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = (
        ('Informations de connexion', {
            'fields': ('email', 'password'),
            'classes': ('wide',)
        }),
        ('Informations personnelles', {
            'fields': ('username', 'first_name', 'last_name'),
            'classes': ('wide',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return obj.get_full_name() or '-'
    full_name.short_description = "Nom complet"

    def account_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Actif</span>')
        return format_html('<span style="color: red;">❌ Inactif</span>')
    account_status.short_description = 'Statut'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    compressed_fields = ['username']
    list_display = ['username', 'email', 'profile_image_display']
    list_display_links = ['username']
    search_fields = ['user__username', 'user__email']

    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',),
            'classes': ('wide',)
        }),
        ('Image de profil', {
            'fields': ('profile_image', 'image_preview'),
            'classes': ('wide',)
        }),
    )

    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                """
                <div style="margin: 10px 0;">
                    <img src="{}" style="max-width: 200px; height: auto; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                </div>
                """,
                obj.profile_image.url
            )
        return format_html(
            '<div style="color: #999; font-style: italic; margin: 10px 0;">Aucune image</div>'
        )
    image_preview.short_description = "Aperçu de l'image"

    def username(self, obj):
        return format_html(
            '<span style="color: #0066cc; font-weight: 500;">{}</span>',
            obj.user.username
        )
    username.short_description = "Nom d'utilisateur"

    def email(self, obj):
        return format_html(
            '<span style="color: #666;">{}</span>',
            obj.user.email
        )
    email.short_description = "Email"

    def profile_image_display(self, obj):
        if obj.profile_image:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 8px; font-size: 0.8em;">✓ Image présente</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 2px 6px; border-radius: 8px; font-size: 0.8em;">❌ Pas d\'image</span>'
        )
    profile_image_display.short_description = 'Image de profil'

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['image_preview']
        if obj:
            readonly_fields.append('user')
        return readonly_fields
