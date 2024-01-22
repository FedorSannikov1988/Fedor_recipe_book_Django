from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)
    account_activation = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1)
    birthday = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        activation: str = 'NOT'

        if self.account_activation:
            activation = 'YES'

        return f'User( ' \
               f'email: {self.email}, ' \
               f'activation: {activation}, ' \
               f'staff: {self.is_staff}, ' \
               f'superuser: {self.is_superuser}' \
               f' )'
