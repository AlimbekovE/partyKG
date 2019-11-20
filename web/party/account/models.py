from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext as _

from party.account.managers import UserManager


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self):
        return self.phone
