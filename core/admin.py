from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignee', 'status', 'deadline', 'created_at', 'updated_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, "Selected tasks have been marked as completed.")
    mark_as_completed.short_description = "Mark selected tasks as completed"