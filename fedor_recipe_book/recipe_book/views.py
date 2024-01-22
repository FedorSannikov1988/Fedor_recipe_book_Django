from django.shortcuts import render


def index(request):

    context = {
        "title": "Книга Рецептов Федора - Главная страница",
    }

    return render(request, 'recipe_book/index.html', context)
