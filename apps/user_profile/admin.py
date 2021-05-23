from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Group


@admin.register(get_user_model())
class UserAdmin(AuthUserAdmin):
    pass


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    fields = ('action_time', 'user', 'content_type', 'action_flag', 'object_id')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.all()

        return self.model.objects.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(Group)
