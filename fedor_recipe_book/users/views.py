from users.models import Users
from django.conf import settings
from smtplib import SMTPException
from django.db import DatabaseError
from users.forms import ChooseRecipe, \
    EnteringEmail, \
    ChooseComment, \
    UploadUserPhoto, \
    UserRegistration, \
    ChangeUserPassword, \
    ChangeUserInformation, \
    UserLogInPersonalAccount, \
    EnteringNewPasswordToRecover
from django.shortcuts import render, \
                             redirect, \
                             get_object_or_404
from recipe_book.models import Recipes, \
                               CommentsOnRecipe, \
                               RecipeCategories
from django.contrib.messages import error, \
                                    success
from django.contrib.auth import login, \
                                logout, \
                                authenticate, \
                                update_session_auth_hash
from recipe_book.forms import AddOneRecipes, \
                              AddOneRecipesV2
from fedor_recipe_book.utilities import WorkingWithToken, \
                                        WorkingWithFiles, \
                                        WorkingWithTimeInsideApp
from django.contrib.auth.decorators import login_required


def user_registration(request):

    if request.method == 'POST':

        form = UserRegistration(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']

            try:

                form.sending_email_activate_account()
                form.save()

                new_user = Users.objects.get(email=email)
                new_user.is_active = False
                new_user.save()

                message_success_for_user: str = \
                    f'На {email} отправлено письмо с ' \
                    f'{settings.EMAIL_HOST_USER} для ' \
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
                    f"Пользователь создан, но" \
                    f"не получилось отправить письмо c" \
                    f"{settings.EMAIL_HOST_USER}" \
                    f"для активации аккаунта."
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
                        'учетная запись не активирована.'
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
                    f"На электронную почту {email} c " \
                    f"{settings.EMAIL_HOST_USER} " \
                    f"отправлено письмо содержащее " \
                    f"ссылку для востановления пароля."
                success(request, message_success_for_user)

            elif search_user and not search_user.is_active:

                message_error_for_user: str = \
                    "Учетная запись не активирована."
                error(request, message_error_for_user)

            else:
                message_error_for_user: str = \
                    "Учетной записи с таким адресом " \
                    "электронной почты не существует."
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

    user = Users.objects.get(email=email)

    all_recipes_user = Recipes.objects.filter(author=user).all()

    all_fields_form_change_user_information = \
        get_all_fields_in_form(ChangeUserInformation())

    all_fields_form_change_user_password = \
        get_all_fields_in_form(ChangeUserPassword(user=user))

    all_fields_form_choose_recipe = \
        get_all_fields_in_form(ChooseRecipe())

    all_fields_form_choose_comment = \
        get_all_fields_in_form(ChooseComment())

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

        else:
            error_message_output(request,
                                 form_change_user_information.errors)

    elif request.method == 'POST' and \
        all(field in request.POST for field in
            all_fields_form_change_user_password):

        form_change_user_password = \
            ChangeUserPassword(user=request.user, data=request.POST)

        if form_change_user_password.is_valid():

            form_change_user_password.save()

            message_success_for_user: str = \
                "Ваш пароль изминен."
            success(request, message_success_for_user)

            update_session_auth_hash(request, request.user)

        else:
            error_message_output(request,
                                 form_change_user_password.errors)

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
        else:
            error_message_output(request,
                                 form_upload_user_photo.errors)

    elif request.method == 'POST' and \
            'delete_user_photo' in request.POST:

        if user.image:
            WorkingWithFiles(path_to_file=
                             user.image.path).delete_file()
            user.image.delete()

    elif request.method == 'POST' and \
            'delete_user_account' in request.POST:

        user.is_active = False
        user.save()
        logout(request)
        return redirect('index')

    elif request.method == 'POST' and \
            all(field in request.POST for field in
                all_fields_form_choose_recipe):

        form_choose_recipe = \
            ChooseRecipe(email_user=user.email,
                         data=request.POST)

        if form_choose_recipe.is_valid():

            choose_recipe = \
                form_choose_recipe.cleaned_data['choose_recipe']

            select_an_action = \
                form_choose_recipe.cleaned_data['select_an_action_for_recipe']

            if select_an_action == 'delete_recipe':

                 search_recipe = \
                     Recipes.objects.get(id=int(choose_recipe))

                 if search_recipe:

                     if search_recipe.image:
                         WorkingWithFiles(path_to_file=
                                          search_recipe.image.path).delete_file()

                     search_recipe.delete()

                     message_success_for_user: str = \
                         "Рецепт удален"
                     success(request, message_success_for_user)

            elif select_an_action == 'change_recipe':

                return redirect('users:editing_recipe_v2', recipe_id=int(choose_recipe))

        else:
            error_message_output(request,
                                 form_choose_recipe.errors)

    elif request.method == 'POST' and \
            all(field in request.POST for field in
                all_fields_form_choose_comment):

        form_choose_comment = \
            ChooseComment(email_user=user.email,
                          data=request.POST)

        if form_choose_comment.is_valid():

            choose_comment = \
                form_choose_comment.cleaned_data['choose_comment']

            select_an_action = \
                form_choose_comment.cleaned_data['select_an_action_for_comment']

            if select_an_action == 'delete_comment':

                 search_comment = \
                     CommentsOnRecipe.objects.get(id=int(choose_comment))

                 if search_comment:
                     search_comment.delete()

                     message_success_for_user: str = \
                         "Комментарий удален"
                     error(request, message_success_for_user)
            elif select_an_action == 'change_comment':
                print("меняем рецепт")
                pass
                #return redirect('users:editing_recipe_v2', recipe_id=int(choose_comment))

        else:
            error_message_output(request,
                                 form_choose_comment.errors)

    form_change_user_information = \
        ChangeUserInformation(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender,
                'birthday': str(user.birthday)
            })

    context = {
        "title": f"Книга Рецептов Федора - Личный кабинет {user.email}",
        "form_change_user_information": form_change_user_information,
        "form_change_user_password": ChangeUserPassword(user=user),
        "form_upload_user_photo": UploadUserPhoto(),
        "form_choose_recipe": ChooseRecipe(email_user=user.email),
        "form_choose_comment": ChooseComment(email_user=user.email),
        "all_recipes_user": all_recipes_user,
        "user": user
    }
    return render(request, 'users/personal_account.html', context)


def error_message_output(request, errors) -> None:

    all_errors: errors = ''

    for title_field_where_error in list(errors.keys()):
        all_errors += errors.get(title_field_where_error)

    error(request, all_errors)


def get_all_fields_in_form(form) -> list:
    return list(form.fields.keys())


@login_required
def exit_personal_account(request):
    logout(request)
    return redirect('index')


@login_required
def editing_recipe(request, recipe_id: int):

    recipe = \
        get_object_or_404(Recipes, id=recipe_id)

    categories_recipe = \
        RecipeCategories.objects.filter(recipes=recipe).first()

    if request.method == 'POST':

        form = \
            AddOneRecipes(request.POST, request.FILES)

        if form.is_valid():

            recipe.title = form.cleaned_data["title"]
            recipe.description = form.cleaned_data["description"]
            recipe.cooking_steps = form.cleaned_data["cooking_steps"]
            recipe.products = form.cleaned_data["products"]
            recipe.cooking_time_in_minutes = form.cleaned_data["cooking_time_in_minutes"]

            recipe.save()

            if 'image' in request.FILES:
                image_file = request.FILES['image']

                if recipe.image:
                    WorkingWithFiles(path_to_file=
                                     recipe.image.path).delete_file()

                recipe.image.save(image_file.name, image_file)

            categories_recipe.recipes.remove(recipe)

            recipe_categories = \
                form.cleaned_data["recipe_categories"]

            if recipe_categories:
                categories_recipe = \
                    RecipeCategories.objects.get(title=recipe_categories)
            else:
                categories_recipe = \
                    RecipeCategories.objects.get(title='Без категории')

            categories_recipe.recipes.add(recipe)

            return redirect('users:personal_account')

    else:

        form = AddOneRecipes(
            initial={
                'recipe_categories': categories_recipe,
                'title': recipe.title,
                'description': recipe.description,
                'cooking_steps': recipe.cooking_steps,
                'products': recipe.products,
                'cooking_time_in_minutes': recipe.cooking_time_in_minutes,
            })

    context = {
        "title": "Книга Рецептов Федора - Личный кабинет - Редактирование рецепта",
        "recipe_id": recipe_id,
        "form": form
    }

    return render(request, 'users/editing_recipe.html', context)


@login_required
def editing_recipe_v2(request, recipe_id: int):

    recipe = \
        get_object_or_404(Recipes, id=recipe_id)

    if request.method == 'POST':

        form = \
            AddOneRecipesV2(request.POST, request.FILES)

        if form.is_valid():

            recipe.title = form.cleaned_data["title"]
            recipe.description = form.cleaned_data["description"]
            recipe.cooking_steps = form.cleaned_data["cooking_steps"]
            recipe.products = form.cleaned_data["products"]
            recipe.cooking_time_in_minutes = form.cleaned_data["cooking_time_in_minutes"]

            recipe.save()

            if 'image' in request.FILES:
                image_file = request.FILES['image']

                if recipe.image:
                    WorkingWithFiles(path_to_file=
                                     recipe.image.path).delete_file()

                recipe.image.save(image_file.name, image_file)

            categories_recipe = \
                RecipeCategories.objects.filter(recipes=recipe).all()

            for one_categories_recipe in categories_recipe:
                one_categories_recipe.recipes.remove(recipe)

            received_recipe_categories = \
                form.cleaned_data["recipe_categories"]

            lisl_recipe_categories: list = []

            if received_recipe_categories:
                for one_recipe_categories in received_recipe_categories:
                    lisl_recipe_categories.append(
                        RecipeCategories.objects.get(id=
                                                     int(one_recipe_categories))
                    )
            else:
                lisl_recipe_categories.append(
                    RecipeCategories.objects.get(title=
                                                 'Без категории')
                )

            for one_recipe_categories in lisl_recipe_categories:
                one_recipe_categories.recipes.add(recipe)

            return redirect('users:personal_account')

    else:

        form = AddOneRecipesV2(
            initial={
                'title': recipe.title,
                'description': recipe.description,
                'cooking_steps': recipe.cooking_steps,
                'products': recipe.products,
                'cooking_time_in_minutes': recipe.cooking_time_in_minutes,
            })

    context = {
        "title": "Книга Рецептов Федора - Личный кабинет - Редактирование рецепта",
        "recipe_id": recipe_id,
        "form": form
    }

    return render(request, 'users/editing_recipe_v2.html', context)


def information_about_author(request, user_id: int):

    user = \
        get_object_or_404(Users, id=user_id)

    all_recipes_user = \
        Recipes.objects.filter(author=user).all()

    context = {
        "title": f"Книга Рецептов Федора - Информация о {user.email}",
        "all_recipes_user": all_recipes_user,
        "user": user
    }
    return render(request, 'users/information_about_author.html', context)