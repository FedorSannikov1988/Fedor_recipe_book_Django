from users.models import Users
from django.conf import settings
from smtplib import SMTPException
from django.db import DatabaseError
from django.shortcuts import render
from users.forms import UserRegistration, \
    UserLogInPersonalAccount, EnteringEmail
from django.contrib.messages import success, error
from django.contrib.auth import authenticate, login
from fedor_recipe_book.utilities import WorkingWithToken, \
                                        WorkingWithTimeInsideApp


def user_registration(request):

    if request.method == 'POST':

        form = UserRegistration(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']

            try:

                form.sending_email_activate_account()
                form.save(commit=True)

                message_success_for_user: str = \
                    f'На {email} отправлено письмо для ' \
                    f'активации аккаунта.'
                success(request, message_success_for_user)

            except DatabaseError:

                message_error_for_user: str = \
                    "Пользователь не зарегистрирован. " \
                    "Произошла неисвестная ошибка " \
                    "(данные не были сохранены в базе данных)."
                error(request, message_error_for_user)

            except SMTPException:

                message_error_for_user: str = \
                    "Пользователь создан, но" \
                    "не получилось отправить письмо " \
                    "для активации аккаунта."
                error(request, message_error_for_user)

            form = UserRegistration()

    else:
        form = UserRegistration()

    context = {
        "title": f"Книга Рецептов Федора - Регистрация Пользователя",
        "form": form
    }

    return render(request, 'users/user_registration.html', context)


def account_activation(request, token: str):

    data: dict = \
        WorkingWithToken().get_data_from_token(token)

    destiny: str = \
        data.get('destiny')

    email: str = \
        data.get('email')

    date_and_time_registration_user: str = \
        data.get('date_and_time')

    if email and destiny and date_and_time_registration_user:

        if WorkingWithTimeInsideApp().checking_date_and_time_registration_user(
            date_and_time_registration_user=date_and_time_registration_user) \
                and destiny == 'user_registration':

            user_search = Users.objects.filter(email=email).first()

            if user_search:

                if not user_search.is_active:

                    user_search.is_active = True

                    try:
                        user_search.save()

                        message_success_for_user: str = \
                            'Ваша учетная запись активирована !'
                        success(request, message_success_for_user)

                    except DatabaseError:

                        message_error_for_user: str = \
                            "Произошла неизвестная ошибка " \
                            "при работе с базой данных." \
                            "Обратитесь к администратору ресурса."
                        error(request, message_error_for_user)

                elif user_search.is_active:

                    message_error_for_user: str = \
                        "Ранее Вы уже активировали " \
                        "свою учетную запись."
                    error(request, message_error_for_user)
            else:
                message_error_for_user: str = \
                    "Пользователь не найден."
                error(request, message_error_for_user)

        elif WorkingWithTimeInsideApp().checking_date_and_time_registration_user(
            date_and_time_registration_user=date_and_time_registration_user) \
                and destiny != 'user_registration':

            message_error_for_user: str = \
                "Ваша ссылка не предназначена " \
                "для активации аккаунта " \
                "(возможно это ссылка " \
                "восстановления пароля)."
            error(request, message_error_for_user)

        else:
            message_error_for_user: str = \
                f'Ваша ссылка для активации учетной записи просрочена.' \
                f'Ссылка акуальна только {settings.TIME_TO_ACTIVATE_ACCOUNT_HOURS} ' \
                f'час(-а)(-ов) с момента регистрации. Обратитесь к администратору сайта.'
            error(request, message_error_for_user)

    else:
        message_error_for_user: str = \
            "Ваша ссылка не валидна " \
            "(Вы потеряли часть текста ссылки)."
        error(request, message_error_for_user)

    context = {
        "title": f"Книга Рецептов Федора - Активация аккаунта",
    }
    return render(request, 'users/account_activation.html', context)


def log_in_personal_account(request):

    if request.method == 'POST':

        form = UserLogInPersonalAccount(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email,
                                password=password)
            if user:
                print("Пользователь вошол в аккаунт !")
                #login(request, user)
                #return HttpResponseRedirect(reverse('users:account'))
            else:
                if Users.objects.filter(email=email).exists():
                    message_error_for_user: str = \
                        'Неверный пароль или ' \
                        'учетная запись не ' \
                        'активирована.'
                else:
                    message_error_for_user: str = \
                        'Учетной записи с таким именем ' \
                         'пользователя (email) нет в базе ' \
                        'данных.'
                error(request, message_error_for_user)

    else:

        form = UserLogInPersonalAccount()

    context = {
        "title": f"Книга Рецептов Федора - Вход в личный кабинет",
        "form": form
    }
    return render(request, 'users/log_in_personal_account.html', context)


def forgot_password(request):

    if request.method == 'POST':

        form = EnteringEmail(request.POST)

        if form.is_valid():
            pass

    else:
        form = EnteringEmail()

    context = {
        "title": f"Книга Рецептов Федора - Забыли пароль ?",
        "form": form
    }
    return render(request, 'users/forgot_password.html', context)
