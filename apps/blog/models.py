from django.conf import settings
from django.db import models
from django.db.models import QuerySet, Count, Q
from tinymce.models import HTMLField


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
        default_permissions = ()


class PostManager(models.Manager):
    def all_with_reactions(self) -> QuerySet['Post']:
        return self.annotate(
            likes=Count('reactions', filter=Q(reactions__reaction_type=PostReaction.LIKE)),
            dislikes=Count('reactions', filter=Q(reactions__reaction_type=PostReaction.DISLIKE))
        )


class Post(models.Model):
    title = models.CharField('Назва', max_length=255, db_index=True)
    content = HTMLField('Вміст')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True,
                                   verbose_name='Створено користувачем')
    preview = models.ImageField(upload_to='post_previews')
    categories = models.ManyToManyField('blog.Category', blank=True, verbose_name='Категорії', related_name='posts')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)

    objects = PostManager()

    def __str__(self) -> str:
        return self.title

    def user_already_reacted(self, user_id: int) -> bool:
        return self.reactions.filter(reacted_by_id=user_id).exists()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        default_permissions = ()


class PostReaction(models.Model):
    LIKE = 0
    DISLIKE = 1

    REACTION_CHOICES = (
        (LIKE, 'Сподобалося'),
        (DISLIKE, 'Не сподобалося'),
    )

    post = models.ForeignKey(Post, models.CASCADE, related_name='reactions')
    reaction_type = models.PositiveSmallIntegerField(choices=REACTION_CHOICES)
    reacted_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)

    class Meta:
        default_permissions = ()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    content = models.TextField('Зміст коментару', max_length=500)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name='Користувач')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children',
                               verbose_name='Коментар, до якого відповідають', null=True, blank=True)

    def __str__(self):
        return f'Коментар від {self.created_by.username} в {self.created_at}'

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        default_permissions = ()


class Category(models.Model):
    COLOR_CHOICES = (
        ('ff0000', 'Червоний'),
        ('00ff00', 'Зелений'),
        ('0000ff', 'Синій')
    )

    title = models.CharField('Назва', max_length=60, db_index=True)
    color = models.CharField('Колір', max_length=6, choices=COLOR_CHOICES)
    preview = models.ImageField(upload_to='category_images/')
    description = models.TextField('Опис', max_length=500)

    def __str__(self) -> str:
        return f'Категорія: "{self.title}"'

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        unique_together = ('title', 'color')
        default_permissions = ()
