from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin


# Reference from : https://docs.djangoproject.com/en/4.2/topics/auth/customizing

class MyUserAdmidn(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'mobile', 'is_admin', 'is_active']
    list_filter = ["is_admin"]
    fieldsets = [   # These are the Layout appear in admin page
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "mobile"]}),
        ("Permissions", {"fields": ["is_admin", "is_active"]}),
    ]
    add_fieldsets = [ # These fields will be appear while adding new user
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "mobile", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"] # Search bar based on Email
    ordering = ["name"] # It will order the fields based on Name

admin.site.register(MyUser, MyUserAdmidn)