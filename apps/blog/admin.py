from django.contrib import admin

from apps.blog.models import Post, Company, Category, Comment


class DefaultUserPermissionsMixin:
    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.all()

        return self.model.objects.filter(created_by=request.user)

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return request.user.is_superuser or request.user == obj.created_by

        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return request.user.is_superuser or request.user == obj.created_by

        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.created_by = request.user

        return super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(DefaultUserPermissionsMixin, admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(DefaultUserPermissionsMixin, admin.ModelAdmin):
    readonly_fields = ('post', 'created_by', 'parent')

    def has_add_permission(self, request):
        return False


admin.site.register(Company)
admin.site.register(Category)
