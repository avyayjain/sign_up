from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email")
        user = self.model()
        user.email = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser):

    email = models.EmailField(unique=True)
    is_opsuser = models.BooleanField(default=False)
    is_clientuser = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

