from django import forms
from django.db import OperationalError
from django.db.utils import DatabaseError
from recipe_book.models import RecipeCategories


class AddOneRecipesV2(forms.Form):

    try:
        all_categories_recipes = RecipeCategories.objects.all()

        all_categories_recipes_for_choices: list = \
            [(one_categories.pk, one_categories.title) for one_categories in all_categories_recipes]

    except DatabaseError or OperationalError:
        all_categories_recipes_for_choices = []
    except:
        all_categories_recipes_for_choices = []

    recipe_categories = forms.MultipleChoiceField(
                                                  required=True,
                                                  label='Категория (обязательное поле):',
                                                  widget=forms.SelectMultiple(
                                                  attrs={'class': 'form_add_one_recipes__multiple_choice_field'}),
                                                  choices=all_categories_recipes_for_choices
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
                        label='Время готовки минут (обязательное поле)',
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

    def clean_recipe_categories(self):
        recipe_categories = self.cleaned_data.get('recipe_categories')

        if not recipe_categories:
            raise forms.ValidationError("Нужно выбрать хотя бы одну категорию из списка")

        recipe_categories_int = int(recipe_categories[0])

        try:
            search_recipe_categories = \
                RecipeCategories.objects.get(id=recipe_categories_int)

        except RecipeCategories.DoesNotExist:
            raise forms.ValidationError("Выбранной категории не существует в базе данных.")

        return recipe_categories

    def update_recipe_categories_choices(self):

        try:
            all_categories_recipes = RecipeCategories.objects.all()
            all_categories_recipes_for_choices: list = \
                [(one_categories.pk, one_categories.title) for one_categories in all_categories_recipes]
        except OperationalError:
            all_categories_recipes_for_choices = []

        self.fields['recipe_categories'].choices = all_categories_recipes_for_choices


class AddOneCommentOnRecipe(forms.Form):

    comment = \
        forms.CharField(
                        required=True,
                        min_length=1,
                        max_length=2000,
                        label='Оставить комментарий',
                        widget=forms.Textarea(
                            attrs={'class': 'content-for-recipe__form_add_one_comment',
                                   'placeholder': 'Введите комментарий не более '
                                                  '2000 символов'}),
    )
