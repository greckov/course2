from django.contrib import admin

from apps.blog.models import Post, Company, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('likes', 'dislikes')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company)
admin.site.register(Category)
