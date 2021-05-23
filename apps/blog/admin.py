from django.contrib import admin

from apps.blog.models import Post, Company, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('likes', 'dislikes')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Post.objects.all()

        return Post.objects.filter(created_by=request.user)

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return request.user.is_superuser or request.user == obj.created_by

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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company)
admin.site.register(Category)
