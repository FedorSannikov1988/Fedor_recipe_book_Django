from django.urls import path
from users.views import editing_recipe, \
                        forgot_password, \
                        personal_account, \
                        user_registration, \
                        account_activation, \
                        exit_personal_account, \
                        entering_new_password, \
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
    path("entering_new_password/<str:token>/",
         entering_new_password, name='entering_new_password'),
    path("personal_account/",
         personal_account, name='personal_account'),
    path("exit_personal_account/",
         exit_personal_account, name='exit_personal_account'),
    path("editing_recipe/<int:recipe_id>/",
         editing_recipe, name='editing_recipe'),
]
