from django import forms
from recipe_book.models import RecipeCategories


class AddOneRecipes(forms.Form):

    recipe_categories = \
        forms.ModelChoiceField(
                        initial=RecipeCategories.objects.get(title='Без категории'),
                        required=False,
                        label='Категория (не обязательное поле):',
                        queryset=RecipeCategories.objects.all(),
                        empty_label='выберите категорию',
                        widget=forms.Select(
                            attrs={'class': 'form_add_one_recipes__drop-down_list'}),

    )

    title = \
        forms.CharField(
                        required=True,
                        min_length=3,
                        max_length=50,
                        label='Название рецепта',
                        widget=forms.TextInput(
                            attrs={'class': 'form_add_one_recipes',
                                   'placeholder': 'Название рецепта (обязательное поле)'}),
    )

    description = \
        forms.CharField(
                        required=True,
                        min_length=3,
                        max_length=1000,
                        label='Краткое описание рецепта',
                        widget=forms.Textarea(
                            attrs={'class': 'form_add_one_recipes__description',
                                   'placeholder': 'Введите краткое не более 1000 '
                                                  'символов описание рецепта '
                                                  '(обязательное поле)'}),
    )

    cooking_steps = \
        forms.CharField(
                        required=True,
                        label='Содержание рецепта',
                        widget=forms.Textarea(
                            attrs={'class': 'form_add_one_recipes__cooking_steps',
                                   'placeholder': 'Введите сам рецепт (обязательное поле)'}),
    )

    products = \
        forms.CharField(
                        required=False,
                        label='Необходимые продукты',
                        widget=forms.Textarea(
                            attrs={'class': 'form_add_one_recipes__description',
                                   'placeholder': 'Введите необходимые для приготовлдения '
                                                  'рецепта продукты (не обязательное поле)'}),
    )

    cooking_time_in_minutes = \
        forms.IntegerField(
                        required=True,
                        label='Время приготовления (обязательное поле)',
                        widget=forms.NumberInput(
                            attrs={'class': 'form_add_one_recipes__cooking_time_in_minutes', 'min': 1})
    )

    image = \
        forms.ImageField(
                        required=False,
                        label='Фотография блюда (не обязательное поле)',
                        widget=forms.FileInput(
                            attrs={'class': 'form_add_one_recipes__image'})

    )
