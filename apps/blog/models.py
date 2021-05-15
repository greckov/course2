from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField('Назва', max_length=100, primary_key=True)
    description = models.TextField(blank=True, max_length=2500)
    site = models.URLField('URL сайта', blank=True)
    email = models.EmailField('Електронна пошта')


class Post(models.Model):
    title = models.CharField('Назва', max_length=255, db_index=True)
    content = models.TextField('Вміст')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True,
                                   verbose_name='Створено користувачем')
    likes = models.IntegerField('Лайки')
    dislikes = models.IntegerField('Дизлайки')
    preview = models.ImageField(upload_to='post_previews')
    categories = models.ManyToManyField('blog.Category', blank=True, verbose_name='Категорії')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    content = models.TextField('Зміст коментару', max_length=500)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name='Користувач')
    created_at = models.DateTimeField(auto_now_add=True, name='Дата створення')


class Category(models.Model):
    COLOR_CHOICES = (
        ('ff0000', 'Червоний'),
        ('00ff00', 'Зелений'),
        ('0000ff', 'Синій')
    )

    title = models.CharField('Назва', max_length=60, db_index=True)
    color = models.CharField('Колір', max_length=6, choices=COLOR_CHOICES)
    description = models.TextField(max_length=500)

    class Meta:
        unique_together = ('title', 'color')
