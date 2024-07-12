# Django admin customization

from django.contrib import admin
# importing base class from default django auth system
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Integrates with django translation system. Anywhere we use _, it will automatically translate text. Not using in our code, but helpful in case we want to use translation in the future
from django.utils.translation import gettext_lazy as _

# imports the custom models we want to register with django admin
from core import models

class UserAdmin(BaseUserAdmin):
    # Define the admin pages for users
    ordering = ['id']
    list_display = ['email', 'name']
    # customized the fieldsets and only use fields that we have in our user model
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
            }
        ),
    )

# Register all pages you want rendered on the admin site
# Need to specify UserAdmin to have custom User admin page
admin.site.register(models.User, UserAdmin)