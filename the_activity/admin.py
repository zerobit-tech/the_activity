from django.contrib import admin

# Register your models here.



from .models import UserActivity




@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj = None):
        return False

    def has_delete_permission(self, request, obj = None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj = None):
        return request.user.is_superuser


    list_display = [
        'action_time',
        'user',
        'change_message',

    ]