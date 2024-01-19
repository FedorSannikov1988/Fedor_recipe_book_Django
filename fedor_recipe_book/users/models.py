from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)
    account_activation = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    gender = models.CharField(max_length=1)

    def __str__(self):
        activation: str = 'not'

        if self.account_activation:
            activation = 'yes'

        return f'Users( ' \
               f'email: {self.email}, ' \
               f'activation: {activation}, ' \
               f'staff: {self.is_staff}, ' \
               f'superuser: {self.is_superuser}' \
               f' )'
