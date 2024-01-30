from users.models import Users
from django.conf import settings
from smtplib import SMTPException
from django.db import DatabaseError
from django.shortcuts import render
from users.forms import UserRegistration
from django.contrib.messages import success, error
from fedor_recipe_book.utilities import WorkingWithTimeInsideApp, \
                                        WorkingWithToken


def user_registration(request):

    if request.method == 'POST':

        form = \
            UserRegistration(request.POST)

        if form.is_valid():

            #form.save(commit=True)

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            birthday = form.cleaned_data['birthday']

            if WorkingWithTimeInsideApp().checking_user_age(date_birth=
                                                            birthday):
                form = UserRegistration()

                user_search = \
                    Users.objects.filter(email=email).first()

                if user_search and \
                        not user_search.is_active:

                    user_search.sending_email_activate_account()

                    message_success_for_user: str = \
                        f'На {email} отправлено письмо для ' \
                        f'восстановления аккаунта.'
                    success(request, message_success_for_user)

                elif user_search and \
                        user_search.is_active:

                    message_error_for_user: str = \
                        "Пользователь c такой электронной " \
                        "почтой уже зарегистрирован."
                    error(request, message_error_for_user)

                else:

                    new_user = Users(
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            gender=gender,
                            birthday=birthday
                    )

                    try:
                        new_user.save()
                        new_user.sending_email_activate_account()

                        message_success_for_user: str = \
                            f'На {email} отправлено письмо для ' \
                            f'активации аккаунта.'
                        success(request, message_success_for_user)

                    except DatabaseError:
                        message_error_for_user: str = \
                            "Пользователь не зарегистрирован. " \
                            "Произошла неисвестная ошибка " \
                            "(данные небыли сохранены в базе данных)."
                        error(request, message_error_for_user)

                    except SMTPException:
                        message_error_for_user: str = \
                            "Пользователь создан, но" \
                            "не получилось отправить письмо " \
                            "для активации аккаунта."
                        error(request, message_error_for_user)

            else:

                message_error_for_user: str = \
                    f"Зарегестрироваться может пользователь от " \
                    f"{settings.LOWER_AGE_YEARS} до " \
                    f"{settings.UPPER_AGE_YEARS} лет"

                error(request, message_error_for_user)

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

        if WorkingWithTimeInsideApp().\
                checking_date_and_time_registration_user(
            date_and_time_registration_user=
            date_and_time_registration_user
        ) and destiny == 'user_registration':

            user_search = \
                Users.objects.filter(email=email).first()

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
                            "Произошла неизвестная ошибка." \
                            "Обратитесь к администратору ресурса."
                        error(request, message_error_for_user)

                elif user_search.is_active:

                    message_error_for_user: str = \
                        "Ранее Вы уже активировали свою " \
                        "учетную запись."
                    error(request, message_error_for_user)

        elif WorkingWithTimeInsideApp().\
                checking_date_and_time_registration_user(
            date_and_time_registration_user=
            date_and_time_registration_user
        ) and destiny != 'user_registration':

            message_error_for_user: str = \
                "Ваша ссылка не предназначена " \
                "для активации аккаунта."
            error(request, message_error_for_user)

        else:
            message_error_for_user: str = \
                f'Ваша ссылка для активации учетной записи просрочена.' \
                f'Ссылка акуальна только {settings.TIME_TO_ACTIVATE_ACCOUNT_HOURS} часа(-ов)' \
                f'с момента регистрации. Обратитесь к администратору сайта.'
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
