from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'display_name',
                    'course', 'student_id', 'auth_type']
    list_filter = ['auth_type', 'course']
    search_fields = ['username', 'first_name', 'last_name', 'student_id']
    fieldsets = UserAdmin.fieldsets + (
        ('Student Info', {'fields': ('student_id', 'course', 'auth_type')}),
    )
