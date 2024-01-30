from django.urls import path
from users.views import user_registration

app_name = 'users'

urlpatterns = [
    path("user_registration/", user_registration, name='user_registration'),
]
