from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.crypto import get_random_string

from rest_framework.authtoken.models import Token
from slugify import slugify

from party.account.managers import UserManager
from party.account.utils import GENDER
from party.api_auth.utils import send_sms_account_verification
from party.locations.models import Region, District, City


class Position(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class User(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True, blank=True, null=True)
    activation_code = models.CharField(max_length=4, blank=True,
                                       verbose_name=_(
                                           'Activation Code'))

    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(choices=GENDER, max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=255, blank=True, null=True)
    plot = models.CharField(max_length=255, blank=True, null=True)
    representation = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self):
        return self.phone

    @classmethod
    def create(cls, phone, password, is_sms_activated=True, **kwargs):
        user = cls(phone=phone, **kwargs)
        user.set_password(password)
        user.activation_code = cls.create_activation_code()
        user.save(is_sms_activation=is_sms_activated)
        return user

    def save(self, *args, **kwargs):
        if kwargs.get('update_fields', None) is None:

            is_sms_activation = kwargs.pop('is_sms_activation', False)

            if is_sms_activation:
                self.send_sms_activation_code(self.activation_code)

        super().save(*args, **kwargs)

    def create_new_password(self, password):
        self.set_password(password)
        self.activation_code = ''
        self.save(update_fields=['activation_code', 'password'])
        return True

    @classmethod
    def create_activation_code(cls):
        code = get_random_string(4, '0123456789')
        if cls.objects.filter(activation_code=code).exists():
            cls.create_activation_code()
        return code

    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception(_('Activation code does not match'))
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])
        return True

    def send_sms_activation_code(self, code):
        send_sms_account_verification(self.phone, code)
        return True

    def get_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token

    @property
    def party_ticket(self):
        region_id = f"{self.region.region_id}".rjust(2, '0') if self.region else "00"
        district_id = f"{self.district.district_id}".rjust(2, '0') if self.district else "00"
        user_id = f"{self.id}".rjust(6, '0')
        return f"{region_id}/{district_id}/{user_id}"

    def get_user_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})


class Avatar(models.Model):
    def user_directory_path(instance, filename):
        return f'accounts/avatars/{instance.user.id}/{filename}'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name = _('Avatar')
        verbose_name_plural = _('Avatars')
