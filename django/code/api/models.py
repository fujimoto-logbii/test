from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib import auth


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('ユーザー名は必須です')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    name = models.CharField(
        verbose_name='氏名',
        max_length=121,
    )

    username = models.CharField(
        verbose_name='ユーザー名',
        max_length=121,
        unique=True,
        help_text='121文字以下で入力してください @/./+/-/_ が使用できます',
        validators=[username_validator],
        error_messages={
            'unique': "ユーザー名が既に使用されています",
        },
    )

    account_name = models.CharField(
        verbose_name='CLIENT NAME',
        max_length=255,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        verbose_name='is_active',
        default=True,
        help_text='ユーザーをアクティブとして扱うかどうかを指定します アカウントを削除する代わりに、これを選択解除します'
    )

    date_joined = models.DateTimeField(
        '追加日',
        default=timezone.now,
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name_plural = 'ユーザー'
        db_table = 'users'

    def __str__(self):
        return self.name
