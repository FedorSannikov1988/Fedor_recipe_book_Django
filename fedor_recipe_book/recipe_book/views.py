import random
from users.models import Users
from django.core.paginator import Paginator
from recipe_book.forms import AddOneRecipes
from django.contrib.messages import success, error
from recipe_book.models import RecipeCategories, Recipes
from django.shortcuts import get_object_or_404, redirect, render


NUMBER_CARDS_PER_PAGE: int = 6
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

    return render(request, 'recipe_book/recipe.html', context)


def recipe_categories(request,
                      id_recipe_categories: int,
                      page_number: int = 1):

    choose_recipe_categories = \
        get_object_or_404(RecipeCategories,
                          id=id_recipe_categories)

    name_selected_category: str = \
        choose_recipe_categories.title

    choose_all_recipe_categories = \
        choose_recipe_categories.recipes.all().order_by('id')

    counter_all_recipes: int = len(choose_all_recipe_categories)

    paginator = \
        Paginator(per_page=NUMBER_CARDS_PER_PAGE,
                  object_list=choose_all_recipe_categories)

    recipe_categories_paginator = \
        paginator.page(page_number)

    total_pages: int = paginator.num_pages

    all_recipe_categories = RecipeCategories.objects.all()

    context = {
        "title": f"Книга Рецептов Федора - {name_selected_category}",
        "recipe_categories_paginator": recipe_categories_paginator,
        "name_selected_category": name_selected_category,
        "all_recipe_categories": all_recipe_categories,
        "id_recipe_categories": id_recipe_categories,
        "counter_all_recipes": counter_all_recipes,
        "total_pages": total_pages,
    }

    return render(request, 'recipe_book/recipe_categories.html', context)


def recipe_search(request,
                  page_number: int = 1,
                  search_query_from_page_number=None):

    question: str = ''
    total_pages: int = 0
    counter_found_recipes: int = 0
    found_recipes_paginator: list = []

    if search_query_from_page_number:
        question = search_query_from_page_number

    else:
        question = request.GET.get('question')

    if question:
        found_recipes = \
            Recipes.objects.filter(title__icontains=question).order_by('title')

        counter_found_recipes: int = len(found_recipes)

        paginator = \
            Paginator(per_page=NUMBER_CARDS_PER_PAGE,
                      object_list=found_recipes)

        found_recipes_paginator = \
            paginator.page(page_number)

        total_pages = paginator.num_pages

    context = {
        "title": f"Книга Рецептов Федора - Поиск Рецепта {question}",
        "found_recipes_paginator": found_recipes_paginator,
        "counter_found_recipes": counter_found_recipes,
        "total_pages": total_pages,
        "question": question
    }

    return render(request, 'recipe_book/recipe_search.html', context)


def add_recipe(request):

    if not request.user.is_authenticated:

        message_error_for_user: str = \
            "Оставить рецепт может только авторизованный, " \
            "а значит зарегестрированный пользователь."
        error(request, message_error_for_user)

        return redirect('users:log_in_personal_account')

    if request.method == 'POST':

        form = AddOneRecipes(request.POST, request.FILES)

        if form.is_valid():

            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            cooking_steps = form.cleaned_data["cooking_steps"]
            products = form.cleaned_data["products"]
            cooking_time_in_minutes = form.cleaned_data["cooking_time_in_minutes"]

            author = Users.objects.get(email=request.user.email)

            recipe = Recipes(title=title,
                             author=author,
                             products=products,
                             description=description,
                             cooking_steps=cooking_steps,
                             cooking_time_in_minutes=
                             cooking_time_in_minutes)

            recipe.save()

            if 'image' in request.FILES:
                image_file = request.FILES['image']
                recipe.image.save(image_file.name, image_file)

            recipe_categories = \
                form.cleaned_data["recipe_categories"]

            if recipe_categories:
                recipe_category = \
                    RecipeCategories.objects.get(title=recipe_categories)
            else:
                recipe_category = \
                    RecipeCategories.objects.get(title='Без категории')

            recipe_category.recipes.add(recipe)

            form = AddOneRecipes()

    else:

        form = AddOneRecipes()

    context = {
        "title": f"Книга Рецептов Федора - Добавить рецепт",
        "form": form
    }

    return render(request, 'recipe_book/add_recipe.html', context)


def my_custom_view_for_400(request, exception):
    return render(request, '400.html')


def my_custom_view_for_403(request, exception):
    return render(request, '403.html', status=403)


def my_custom_view_for_404(request, exception):
    return render(request, '404.html', status=404)


def my_custom_view_for_500(request):
    return render(request, '500.html', status=500)
