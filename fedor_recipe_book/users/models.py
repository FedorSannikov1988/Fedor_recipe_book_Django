from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from fedor_recipe_book.utilities import WorkingWithToken, \
                                        WorkingWithTimeInsideApp


app_label = 'users'


class Users(AbstractUser):
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    gender = models.CharField(max_length=1)
    birthday = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'birthday', 'password']

    def __str__(self):
        return f'User( ' \
               f'email: {self.email}, ' \
               f'active: {self.is_active}, ' \
               f'staff: {self.is_staff}, ' \
               f'superuser: {self.is_superuser}' \
               f' )'

    def sending_email_recover_password(self):

        timestamp: str = \
            WorkingWithTimeInsideApp().get_data_and_time()

        token: str = \
            WorkingWithToken().get_token(data={'destiny': 'password_recovery',
                                                'email': self.email,
                                                'date_and_time': timestamp})

        half_link = reverse("users:entering_new_password",
                            kwargs={"token": token})

        activate_account_link = f"{settings.DOMAIN_NAME}{half_link}"

        subject = \
            f"Восстановление пароля на {settings.DOMAIN_NAME}"

        message = \
            f"Для восстановления пароля " \
            f"перейдите по ссылке: {activate_account_link} ." \
            f" Cсылка активна {settings.DURATION_PASSWORD_RECOVERY_LINK_MINUTES} " \
            f"минут с момента отправки данного письма."

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.email],
            fail_silently=False,
        )


