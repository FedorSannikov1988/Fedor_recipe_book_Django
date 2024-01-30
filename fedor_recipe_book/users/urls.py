from django.urls import path
from users.views import user_registration,\
                        account_activation

app_name = 'users'

urlpatterns = [
    path("user_registration/", user_registration, name='user_registration'),
    path("account_activation/<str:token>/", account_activation, name='account_activation'),
]
