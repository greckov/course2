from django.contrib import admin

from apps.blog.models import Post, Company, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('likes', 'dislikes')


admin.site.register(Company)
admin.site.register(Category)
