from django.db import models
from django.contrib.auth.models import AbstractUser


app_label = 'users'


class Users(AbstractUser):
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    gender = models.CharField(max_length=1)
    birthday = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return f'User( ' \
               f'email: {self.email}, ' \
               f'active: {self.is_active}, ' \
               f'staff: {self.is_staff}, ' \
               f'superuser: {self.is_superuser}' \
               f' )'
