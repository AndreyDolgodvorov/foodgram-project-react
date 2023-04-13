from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    USER_ROLE = [
        (USER, 'пользователь'),
        (ADMIN, 'администратор')
    ]
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True
    )
    password = models.CharField(
        'Пароль',
        max_length=150
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLE,
        default=USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow')
        ]

    def __str__(self):
        return f'{self.user} {self.author}'