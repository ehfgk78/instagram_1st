from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=40, *args, **kwargs)

class User(AbstractUser):
    img_profile = models.ImageField(
        upload_to='user',
        blank=True
    )
    age = models.IntegerField( blank=True, null=True )

    objects = UserManager()