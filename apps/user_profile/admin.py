from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Group


@admin.register(get_user_model())
class UserAdmin(AuthUserAdmin):
    pass


admin.site.unregister(Group)
