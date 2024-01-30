import datetime
from django import forms
from users.models import Users
from django.contrib.auth.forms import UserCreationForm


#class UserRegistration(forms.Form):
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
                                   'placeholder': 'Пароль'}))

    password2 = forms.CharField(
                        required=True,
                        label="Подтверждение пароля",
                        widget=forms.PasswordInput(
                            attrs={'class': 'form_user_registration_necessary',
                                   'placeholder': 'Подтверждение пароля'}))

    class Meta(UserCreationForm.Meta):
        #model = Users
        fields = ['first_name', 'last_name',
                  'email', 'gender', 'birthday',
                  'password1', 'password2']