import datetime
from django import forms


class UserRegistration(forms.Form):

    current_date = datetime.date.today()
    current_date_string = current_date.strftime("%Y-%m-%d")

    GENDER_CHOICES = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]

    first_name = \
        forms.CharField(min_length=1,
                        max_length=50,
                        label='Имя',
                        widget=forms.TextInput(
                            attrs={'class': 'form_user_registration_not_necessary',
                                   'placeholder': 'Введите Ваше имя (не обязательное поле)'}),
    )

    last_name = \
        forms.CharField(min_length=1,
                        max_length=50,
                        label='Фамилия',
                        widget=forms.TextInput(
                            attrs={'class': 'form_user_registration_not_necessary',
                                   'placeholder': 'Введите Вашу фамилию (не обязательное поле)'}),
    )

    email = \
        forms.EmailField(
                        label='Электронная почта',
                        widget=forms.EmailInput(
                            attrs={'class': 'form_user_registration_necessary',
                                   'placeholder': 'email@mail.com (обязательное поле)'}),
    )

    gender = \
        forms.ChoiceField(
                        label='Пол (обязательное поле)',
                        choices=GENDER_CHOICES,
                        widget=forms.RadioSelect(
                            attrs={'class': 'form_user_registration_necessary_gender'}),
    )

    birthday = forms.DateField(
                               label="День рождения (обязательное поле)",
                               initial=current_date_string,
                               widget=forms.DateInput(
                                  attrs={'class': 'form_user_registration_necessary_birthday',
                                         'type': 'date'}))
