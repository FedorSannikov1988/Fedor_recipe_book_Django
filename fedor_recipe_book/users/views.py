from django.shortcuts import render
from users.forms import UserRegistration
import datetime


def user_registration(request):

    form = UserRegistration()

    context = {
        "title": f"Книга Рецептов Федора - Регистрация Пользователя",
        "form": form
    }

    return render(request, 'users/user_registration.html', context)
