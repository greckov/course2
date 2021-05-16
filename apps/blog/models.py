from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField('Назва', max_length=100, primary_key=True)
    description = models.TextField('Опис', blank=True, max_length=2500)
    site = models.URLField('URL сайта', blank=True)
    email = models.EmailField('Електронна пошта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компанія'
        verbose_name_plural = 'Компанії'


class Post(models.Model):
    title = models.CharField('Назва', max_length=255, db_index=True)
    content = models.TextField('Вміст')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True,
                                   verbose_name='Створено користувачем')
    likes = models.IntegerField('Лайки', default=0, editable=False)
    dislikes = models.IntegerField('Дизлайки', default=0, editable=False)
    preview = models.ImageField(upload_to='post_previews')
    categories = models.ManyToManyField('blog.Category', blank=True, verbose_name='Категорії')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    content = models.TextField('Зміст коментару', max_length=500)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name='Користувач')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)

    def __str__(self):
        return f'Коментар від {self.created_by.username} в {self.created_at}'

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коменті'


class Category(models.Model):
    COLOR_CHOICES = (
        ('ff0000', 'Червоний'),
        ('00ff00', 'Зелений'),
        ('0000ff', 'Синій')
    )

    title = models.CharField('Назва', max_length=60, db_index=True)
    color = models.CharField('Колір', max_length=6, choices=COLOR_CHOICES)
    description = models.TextField('Опис', max_length=500)

    def __str__(self) -> str:
        return f'Категорія: "{self.title}"'

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        unique_together = ('title', 'color')
