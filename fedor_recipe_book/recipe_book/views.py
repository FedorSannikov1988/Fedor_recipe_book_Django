import random
from django.shortcuts import render, get_object_or_404
from recipe_book.models import RecipeCategories, Recipes


NUMBER_RECIPES_ON_MAIN_PAGE: int = 5


def index(request):

    five_random_recipes: list = []

    all_recipes = Recipes.objects.all()

    all_recipe_categories = RecipeCategories.objects.all()

    len_all_recipes: int = len(all_recipes)

    if len_all_recipes >= NUMBER_RECIPES_ON_MAIN_PAGE:

        while len(five_random_recipes) < NUMBER_RECIPES_ON_MAIN_PAGE:

            random_choice_recipe = random.choice(all_recipes)

            if random_choice_recipe not in five_random_recipes:
                five_random_recipes.append(random_choice_recipe)

    elif 2 <= len_all_recipes < NUMBER_RECIPES_ON_MAIN_PAGE:

        for _ in range(NUMBER_RECIPES_ON_MAIN_PAGE):
            five_random_recipes.append(random.choice(all_recipes))

    elif 0 < len_all_recipes < 2:

        for _ in range(NUMBER_RECIPES_ON_MAIN_PAGE):
            five_random_recipes.append(all_recipes[0])

    context = {
        "title": "Книга Рецептов Федора - Главная Страница",
        "all_recipe_categories": all_recipe_categories,
        "five_random_recipes": five_random_recipes
    }

    return render(request, 'recipe_book/index.html', context)


def contacts(request):

    context = {
        "title": "Книга Рецептов Федора - Контакты разработчика",
    }

    return render(request, 'recipe_book/contacts.html', context)


def recipe(request, id_recipe: int):

    desired_recipe = \
        get_object_or_404(Recipes, id=id_recipe)

    context = {
        "title": f"Книга Рецептов Федора - {desired_recipe.title}",
        "recipe": desired_recipe
    }
    #return render(request, 'recipe_book/contacts.html', context)
    return render(request, 'recipe_book/recipe.html', context)