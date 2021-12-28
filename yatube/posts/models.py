from django.contrib.auth import get_user_model
from django.db import models
from .validators import validate_not_empty

User = get_user_model()


class Post(models.Model):
    """
    Класс Post используется для создания моделей Post
    (пост в социальной сети).
    """
    text = models.TextField(
        max_length=10000,
        validators=[validate_not_empty],
        blank=False
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='postsin',
        blank=True,
        null=True,
    )

    class Meta:
        """
        Внутренний класс Meta для хранения метаданных
        класса Post.
        """
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text


class Group(models.Model):
    """
    Класс Group используется для создания моделей Group
    сообществ, в которых происходит размещение постов
    в социальной сети.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title
