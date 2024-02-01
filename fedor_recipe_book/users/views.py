from pathlib import Path
from users.models import Users
from django.conf import settings
from smtplib import SMTPException
from django.db import DatabaseError
from users.forms import EnteringEmail, \
                        UploadUserPhoto, \
                        UserRegistration, \
                        ChangeUserInformation, \
                        UserLogInPersonalAccount, \
                        EnteringNewPasswordToRecover
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from fedor_recipe_book.utilities import WorkingWithToken, \
                                        WorkingWithFiles, \
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
                login(request, user)
                return redirect('users:personal_account')
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

            email = form.cleaned_data['email']

            search_user = Users.objects.filter(email=email).first()

            if search_user and search_user.is_active:

                search_user.sending_email_recover_password()

                message_success_for_user: str = \
                    f"На электронную почту {email} " \
                    f"отправлено письмо содержащее " \
                    f"ссылку для востановления пароля."
                success(request, message_success_for_user)

            elif search_user and not search_user.is_active:

                message_error_for_user: str = \
                    "Учетная запись не активирована."
                error(request, message_error_for_user)

            else:
                message_error_for_user: str = \
                    f"Учетной записи с таким адресом " \
                    f"электронной почты не существует."
                error(request, message_error_for_user)

    else:
        form = EnteringEmail()

    context = {
        "title": f"Книга Рецептов Федора - Забыли пароль ?",
        "form": form
    }
    return render(request, 'users/forgot_password.html', context)


def entering_new_password(request, token: str):

    form = None

    data: dict = \
        WorkingWithToken().get_data_from_token(token)

    destiny: str = \
        data.get('destiny')

    email: str = \
        data.get('email')

    date_and_time_receipt_request: str = \
        data.get('date_and_time')

    if email and destiny and date_and_time_receipt_request:

        if destiny != 'password_recovery':

            message_error_for_user: str = \
                "Cсылка не предназначена для" \
                "восстановления пароля."
            error(request, message_error_for_user)

        elif WorkingWithTimeInsideApp().checking_time_password_recovery_request(
                time_receipt_request=date_and_time_receipt_request) \
                and destiny == 'password_recovery' \
                and request.method == 'GET':

            form = EnteringNewPasswordToRecover()

        elif WorkingWithTimeInsideApp().checking_time_password_recovery_request(
                time_receipt_request=date_and_time_receipt_request) \
                and destiny == 'password_recovery' \
                and request.method == 'POST':

            form = EnteringNewPasswordToRecover(request.POST)

            if form.is_valid():

                search_user = Users.objects.get(email=email)

                if search_user and search_user.is_active:

                    new_password = form.cleaned_data['password2']
                    search_user.set_password(new_password)

                    try:
                        search_user.save()

                        message_success_for_user: str = \
                            "Ваш пароль изминен."
                        success(request, message_success_for_user)
                        return redirect('users:log_in_personal_account')

                    except DatabaseError:

                        message_error_for_user: str = \
                            "Произошла неизвестная ошибка " \
                            "при работе с базой данных." \
                            "Обратитесь к администратору ресурса."
                        error(request, message_error_for_user)

                elif search_user and not search_user.is_active:

                    message_error_for_user: str = \
                        "Аккаунт пользователя не активен."
                    error(request, message_error_for_user)

                else:
                    message_error_for_user: str = \
                        "Пользователь не найден."
                    error(request, message_error_for_user)

        else:

            message_error_for_user: str = \
                f'Ваша ссылка для восстановления пароля просрочена.' \
                f'Ссылка актуальна ' \
                f'{settings.DURATION_PASSWORD_RECOVERY_LINK_MINUTES} минут.'
            error(request, message_error_for_user)

    else:

        message_error_for_user: str = \
            "Ваша ссылка не валидна " \
            "(Вы потеряли часть текста ссылки)."
        error(request, message_error_for_user)

    context = {
        "title": f"Книга Рецептов Федора - Ввод нового пароля",
        "token": token,
        "form": form
    }
    return render(request, 'users/entering_new_password.html', context)


@login_required
def personal_account(request):

    email = request.user.email

    user = get_object_or_404(Users, email=email)

    all_fields_form_change_user_information = \
        list(ChangeUserInformation().fields.keys())

    print(request.POST)

    if request.method == 'POST' and \
            all(field in request.POST for field in
                all_fields_form_change_user_information):

        form_change_user_information = \
            ChangeUserInformation(request.POST)

        if form_change_user_information.is_valid():

            user.first_name = form_change_user_information.cleaned_data['first_name']
            user.last_name = form_change_user_information.cleaned_data['last_name']
            user.gender = form_change_user_information.cleaned_data['gender']
            user.birthday = form_change_user_information.cleaned_data['birthday']

            user.save()

        context = {
            "title": f"Книга Рецептов Федора - Личный кабинет",
            "form_change_user_information": form_change_user_information,
            "form_upload_user_photo": UploadUserPhoto(),
        }
        return render(request, 'users/personal_account.html', context)

    elif request.method == 'POST' and \
            'image' in request.FILES:

        form_upload_user_photo = \
            UploadUserPhoto(data=request.POST,
                            files=request.FILES)

        if form_upload_user_photo.is_valid():

            image_file = request.FILES['image']

            if user.image:

                WorkingWithFiles(path_to_file=
                                 user.image.path).delete_file()

                user.image.save(image_file.name, image_file)

    form_change_user_information = \
        ChangeUserInformation(
             initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender,
                'birthday': str(user.birthday)
    })

    context = {
        "title": f"Книга Рецептов Федора - Личный кабинет",
        "form_change_user_information": form_change_user_information,
        "form_upload_user_photo": UploadUserPhoto(),
        "user": user
    }
    return render(request, 'users/personal_account.html', context)
