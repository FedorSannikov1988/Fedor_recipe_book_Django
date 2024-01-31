from django.urls import path
from users.views import forgot_password, \
                        user_registration, \
                        account_activation, \
                        log_in_personal_account

app_name = 'users'

urlpatterns = [
    path("user_registration/",
         user_registration, name='user_registration'),
    path("account_activation/<str:token>/",
         account_activation, name='account_activation'),
    path("log_in_personal_account/",
         log_in_personal_account, name='log_in_personal_account'),
    path("forgot_password/",
         forgot_password, name='forgot_password'),
]
