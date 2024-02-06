import datetime
from django import forms
from django.db import OperationalError
from recipe_book.models import Recipes, \
                               CommentsOnRecipe
from users.models import Users
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm, \
                                      PasswordChangeForm
from fedor_recipe_book.utilities import WorkingWithToken, \
                                        WorkingWithTimeInsideApp, \
                                        WorkingWithRegularExpressions


class UserRegistration(UserCreationForm):

    current_date = datetime.date.today()
    current_date_string = current_date.strftime("%Y-%m-%d")

    GENDER_CHOICES = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]

    first_name = \
        forms.CharField(
                        required=False,
                        min_length=1,
                        max_length=50,
                        label='Имя',
                        widget=forms.TextInput(
                            attrs={'class': 'form_user_registration_not_necessary',
                                   'placeholder': 'Введите Ваше имя (не обязательное поле)'}),
    )

    last_name = \
        forms.CharField(
                        required=False,
                        min_length=1,
                        max_length=50,
                        label='Фамилия',
                        widget=forms.TextInput(
                            attrs={'class': 'form_user_registration_not_necessary',
                                   'placeholder': 'Введите Вашу фамилию (не обязательное поле)'}),
    )

    email = \
        forms.EmailField(
                        required=True,
                        label='Электронная почта',
                        widget=forms.EmailInput(
                            attrs={'class': 'form_user_registration_necessary',
                                   'placeholder': 'email@mail.com (обязательное поле)'}),
    )

    gender = \
        forms.ChoiceField(
                        required=True,
                        label='Пол (обязательное поле)',
                        choices=GENDER_CHOICES,
                        widget=forms.RadioSelect(
                            attrs={'class': 'form_user_registration_necessary_gender'}),
    )

    birthday = forms.DateField(
                        required=True,
                        label="День рождения (обязательное поле)",
                        initial=current_date_string,
                        widget=forms.DateInput(
                            attrs={'class': 'form_user_registration_necessary_birthday',
                                    'type': 'date'}))

    password1 = forms.CharField(
                        required=True,
                        label="Пароль",
                        widget=forms.PasswordInput(
                            attrs={'class': 'form_user_registration_necessary',
                                   'placeholder': 'Пароль (обязательное поле)'}))

    password2 = forms.CharField(
                        required=True,
                        label="Подтверждение пароля",
                        widget=forms.PasswordInput(
                            attrs={'class': 'form_user_registration_necessary',
                                   'placeholder': 'Подтверждение пароля (обязательное поле)'}))

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        pattern = r'^[а-яА-ЯёЁ]+$'
        if not WorkingWithRegularExpressions.\
                checking_string(string=first_name,
                                pattern=pattern) and not first_name == "":
            message_error_for_user: str = \
                "Имя может состоять только из букв " \
                "русского алфавита (не какой латиницы " \
                "цифр или пробелов)."
            raise forms.ValidationError(message_error_for_user)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        pattern = r'^[а-яА-ЯёЁ]+$'
        if not WorkingWithRegularExpressions.\
                checking_string(string=last_name,
                                pattern=pattern) and not last_name == "":
            message_error_for_user: str = \
                "Фамилия может состоять только из букв " \
                "русского алфавита (не какой латиницы " \
                "цифр или пробелов)."
            raise forms.ValidationError(message_error_for_user)
        return last_name

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        if not WorkingWithTimeInsideApp().\
                checking_user_age(date_birth=birthday):
            message_error_for_user: str = \
                f"Зарегестрироваться может пользователь от " \
                f"{settings.LOWER_AGE_YEARS} до " \
                f"{settings.UPPER_AGE_YEARS} лет"
            raise forms.ValidationError(message_error_for_user)
        return birthday

    def clean_email(self):
        email = self.cleaned_data.get('email')

        user_search = \
            Users.objects.filter(email=email).first()

        if user_search and not user_search.is_active:

            self.sending_email_activate_account()

            message_error_for_user: str = \
                f'На {email} отправлено письмо для ' \
                f'восстановления аккаунта.'
            raise forms.ValidationError(message_error_for_user)

        elif user_search and user_search.is_active:

            message_error_for_user: str = \
                "Пользователь c такой электронной " \
                "почтой уже зарегистрирован."
            raise forms.ValidationError(message_error_for_user)

        return email

    def sending_email_activate_account(self):
        email = self.cleaned_data.get('email')

        timestamp: str = \
            WorkingWithTimeInsideApp().get_data_and_time()

        token: str = \
            WorkingWithToken().get_token(data={'destiny': 'user_registration',
                                               'email': email,
                                               'date_and_time': timestamp})

        half_link = reverse("users:account_activation",
                            kwargs={"token": token})

        activate_account_link = f"{settings.DOMAIN_NAME}{half_link}"

        subject = \
            f"Активация аккаунта на {settings.DOMAIN_NAME}"

        message = \
            f"Для активация аккаунта " \
            f"перейдите по ссылке: {activate_account_link} ." \
            f" Cсылка активна {settings.TIME_TO_ACTIVATE_ACCOUNT_HOURS} " \
            f"час(-а)(-ов) с момента отправки данного письма."

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ['first_name', 'last_name',
                  'email', 'gender', 'birthday',
                  'password1', 'password2']


class UserLogInPersonalAccount(forms.Form):

    email = \
        forms.EmailField(
                        required=True,
                        label='Электронная почта',
                        widget=forms.EmailInput(
                            attrs={'class': 'form_user_log_in_personal_account',
                                   'placeholder': 'Адрес электронной почты'}),
    )

    password = forms.CharField(
                        required=True,
                        label="Пароль",
                        widget=forms.PasswordInput(
                            attrs={'class': 'form_user_log_in_personal_account',
                                   'placeholder': 'Пароль'}))


class EnteringEmail(forms.Form):

    email = \
        forms.EmailField(
                        required=True,
                        label='Электронная почта',
                        widget=forms.EmailInput(
                            attrs={'class': 'form_entering_email',
                                   'placeholder': 'Адрес электронной почты'}),
    )


class EnteringNewPasswordToRecover(UserCreationForm):

    password1 = forms.CharField(
                        required=True,
                        label="Новый пароль",
                        widget=forms.PasswordInput(
                            attrs={'class': 'form_user_new_password_to_recover',
                                   'placeholder': 'Пароль'}))

    password2 = forms.CharField(
                        required=True,
                        label="Подтверждение пароля",
                        widget=forms.PasswordInput(
                            attrs={'class': 'form_user_new_password_to_recover',
                                   'placeholder': 'Подтверждение пароля'}))

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ['password1', 'password2']


class ChangeUserInformation(forms.Form):

    GENDER_CHOICES = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]

    first_name = \
        forms.CharField(
                        required=False,
                        min_length=1,
                        max_length=50,
                        label='Имя',
                        widget=forms.TextInput(
                            attrs={'class': 'form_user_personal_account_сhange_user_information',
                                   'placeholder': 'Имя (не обязательное поле)', 'name': 'test'}),
    )

    last_name = \
        forms.CharField(
                        required=False,
                        min_length=1,
                        max_length=50,
                        label='Фамилия',
                        widget=forms.TextInput(
                            attrs={'class': 'form_user_personal_account_сhange_user_information',
                                   'placeholder': 'Фамилию (не обязательное поле)'}),
    )

    gender = \
        forms.ChoiceField(
                        required=True,
                        label='Пол (обязательное поле)',
                        choices=GENDER_CHOICES,
                        widget=forms.RadioSelect(
                            attrs={'class': 'form_user_personal_account_сhange_user_information_gender'}),
    )

    birthday = forms.DateField(
                        required=True,
                        label="День рождения (обязательное поле)",
                        widget=forms.DateInput(
                            attrs={'class': 'form_user_personal_account_сhange_user_information_birthday',
                                    'type': 'date'}))

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        pattern = r'^[а-яА-ЯёЁ]+$'
        if not WorkingWithRegularExpressions.\
                checking_string(string=first_name,
                                pattern=pattern):
            message_error_for_user: str = \
                "Имя может состоять только из букв " \
                "русского алфавита (не какой латиницы " \
                "цифр или пробелов между буквами)."
            raise forms.ValidationError(message_error_for_user)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        pattern = r'^[а-яА-ЯёЁ]+$'
        if not WorkingWithRegularExpressions.\
                checking_string(string=last_name,
                                pattern=pattern):
            message_error_for_user: str = \
                "Фамилия может состоять только из букв " \
                "русского алфавита (не какой латиницы " \
                "цифр или пробелов между буквами)."
            raise forms.ValidationError(message_error_for_user)
        return last_name

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        if not WorkingWithTimeInsideApp().\
                checking_user_age(date_birth=birthday):
            message_error_for_user: str = \
                f"Зарегестрироваться может пользователь от " \
                f"{settings.LOWER_AGE_YEARS} до " \
                f"{settings.UPPER_AGE_YEARS} лет"
            raise forms.ValidationError(message_error_for_user)
        return birthday


class UploadUserPhoto(forms.Form):

    image = forms.ImageField(required=False,
                             widget=forms.FileInput(
                                 attrs={'class': 'form_user_personal_account_upload_user_photo'}))


class ChangeUserPassword(PasswordChangeForm):

    old_password = forms.CharField(
                        required=True,
                        label="Старый пароль",
                        widget=forms.PasswordInput(
                            attrs={'class': 'form_user_personal_account_change_user_password',
                                   'placeholder': 'Старый пароль'}))

    new_password1 = forms.CharField(
                        required=True,
                        label="Новый пароль",
                        widget=forms.PasswordInput(
                            attrs={'class': 'form_user_personal_account_change_user_password',
                                   'placeholder': 'Новый пароль'}))

    new_password2 = forms.CharField(
                        required=True,
                        label="Подтверждение нового пароля",
                        widget=forms.PasswordInput(
                            attrs={'class': 'form_user_personal_account_change_user_password',
                                   'placeholder': 'Подтверждение нового пароля'}))


class ChooseRecipe(forms.Form):

    def __init__(self, email_user: str = '', data=None):
        super().__init__(data)

        self.fields['choose_recipe'] = forms.ChoiceField(
                                    required=True,
                                    label='Выши рецепты:',
                                    widget=forms.RadioSelect(
                                        attrs={'class':
                                                'content-for-personal_account__form_choose_recipe__choose_recipe'}),
                                    choices=self.get_choices(email_user=email_user)
        )

    @staticmethod
    def get_choices(email_user: str) -> list:

        if email_user:

            try:
                user = Users.objects.get(email=email_user)

                recipes_user = Recipes.objects.filter(author=user).all()

                result = [(one_recipe.pk, one_recipe.title) for one_recipe in recipes_user]

            except OperationalError:
                result = []

            return result
        else:
            return []

    ACTION = [
        ('go_over_recipe', 'Перейти'),
        ('change_recipe', 'Изменить'),
        ('delete_recipe', 'Удалить'),
    ]

    select_an_action_for_recipe = \
        forms.ChoiceField(
                        required=True,
                        label='Действие',
                        choices=ACTION,
                        widget=forms.RadioSelect(
                            attrs={'class': 'content-for-personal_account__form_choose_recipe__select_an_action'}),
    )


class ChooseComment(forms.Form):

    def __init__(self, email_user: str = '', data=None):
        super().__init__(data)

        self.fields['choose_comment'] = forms.ChoiceField(
                                    required=True,
                                    label='Выши комментарии:',
                                    widget=forms.RadioSelect(
                                        attrs={'class':
                                                'content-for-personal_account__form_choose_recipe__choose_recipe'}),
                                    choices=self.get_choices(email_user=email_user)
        )

    @staticmethod
    def get_choices(email_user: str) -> list:

        if email_user:

            try:
                user = Users.objects.get(email=email_user)

                comments_user = CommentsOnRecipe.objects.filter(author=user).all()

                result =  \
                    [(one_comment_user.id, ChooseComment.generating_string(one_comment_user))
                     for one_comment_user in comments_user]

            except OperationalError:
                result = []

            return result
        else:
            return []

    @staticmethod
    def generating_string(one_comment_user) -> str:
        return "Рецепт: " + str(one_comment_user.recipe.title) + " - " + \
               "Создан: " + str(one_comment_user.date_creation.strftime("%d.%m.%Y")) + " - " + \
               "Изминен: " + str(one_comment_user.date_change.strftime("%d.%m.%Y")) + " - " + \
               "Комментарий: " + str(one_comment_user.comment)

    ACTION = [
        ('go_over_comment', 'Перейти'),
        ('change_comment', 'Изменить'),
        ('delete_comment', 'Удалить'),
    ]

    select_an_action_for_comment = \
        forms.ChoiceField(
                        required=True,
                        label='Действие',
                        choices=ACTION,
                        widget=forms.RadioSelect(
                            attrs={'class': 'content-for-personal_account__form_choose_recipe__select_an_action'}),
    )