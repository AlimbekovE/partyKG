from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError(_('Please provide phone'))
        user = self.model(phone=phone,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, user_type, password):
        if not phone:
            raise ValueError(_('Please provide phone'))
        user = self.model(phone=phone, is_staff=True, is_active=True)
        user.set_password(password)
        user.save(using=self._db)
        return user
