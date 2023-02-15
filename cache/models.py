import datetime
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.core.exceptions import FieldError
from django.db import models

from mjlkart import settings


# class ArchivedManager(models.Manager):
#     def get_queryset(self):
#         queryset = super(ArchivedManager, self).get_queryset().filter(is_deleted=False)
#         try:
#             qs = queryset.filter(is_archive=True)
#         except FieldError:
#             qs = queryset
#
#         # request = get_request()
#
#         return qs
#
#
# class DeletedManager(models.Manager):
#     def get_queryset(self):
#         qs = super(DeletedManager, self).get_queryset().filter(is_delete=True)
#
#         # request = get_request()
#
#         return qs


class AccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Email address is required')

        if not username:
            raise ValueError('Username is required')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.EmailField(max_length=50, blank=False, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = AccountManager()

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class DefaultField(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(blank=True)
    date_deleted = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.date_modified = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        self.full_clean()
        super(DefaultField, self).save()
        return super(DefaultField, self).save()

    # def delete(self, using=None, keep_parents=False):
    #     self.is_deleted = True
    #     self.date_deleted = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    #     self.save()
    #     return
