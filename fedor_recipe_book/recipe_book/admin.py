from django.contrib import admin
from recipe_book.models import Recipes, \
                               RecipeCategories, \
                               CommentsOnRecipe


@admin.register(CommentsOnRecipe)
class CommentsOnRecipeAdmin(admin.ModelAdmin):
    list_display = ["author", "recipe", "date_creation", "date_change"]
    ordering = ["date_creation", "date_change"]
    list_filter = ["date_creation", "date_change"]
    search_fields = ["comment"]
    search_help_text = "Поиск по полю comment (содержание комментария)"

    readonly_fields = ["date_creation", "date_change"]
    fieldsets = [
        (
            'Рецепт',
            {
                'classes': ['wide'],
                'fields': ['recipe'],
            },
        ),
        (
            'Автор',
            {
                'classes': ['wide'],
                'fields': ['author'],
            },
        ),
        (
            'Комментарий',
            {
                'classes': ['wide'],
                'fields': ['comment'],
            },
        ),
        (
            'Дата создания',
            {
                'classes': ['wide'],
                'fields': ['date_creation'],
            },
        ),
        (
            'Дата изминнения',
            {
                'classes': ['wide'],
                'fields': ['date_change'],
            },
        ),
    ]


@admin.register(RecipeCategories)
class RecipeCategoriesAdmin(admin.ModelAdmin):
    list_display = ["title"]
    ordering = ["title"]
    list_filter = ["title"]
    search_fields = ["title"]
    search_help_text = "Поиск по полю title"

    fieldsets = [
        (
            'Название',
            {
                'classes': ['wide'],
                'fields': ['title'],
            },
        ),
        (
            'Все рецепты в данной категории',
            {
                'classes': ['wide'],
                'fields': ['recipes'],
            },
        ),
    ]


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ["title", "cooking_time_in_minutes", "author", "about_image"]
    ordering = ["author"]
    list_filter = ["title", "author"]
    search_fields = ["title"]
    search_help_text = "Поиск по полю title"
    actions = ["delete_title", "delete_description",
               "delete_cooking_steps", "delete_products",
               "delete_image"]

    fieldsets = [
        (
            'Название',
            {
                'classes': ['wide'],
                'fields': ['title'],
            },
        ),
        (
            'Описание',
            {
                'classes': ['wide'],
                'fields': ['description'],
            },
        ),
        (
            'Шаги приготовления',
            {
                'classes': ['wide'],
                'fields': ['cooking_steps'],
            },
        ),
        (
            'Продукты',
            {
                'classes': ['wide'],
                'fields': ['products'],
            },
        ),
        (
            'Время приготовления',
            {
                'classes': ['wide'],
                'fields': ['cooking_time_in_minutes'],
            },
        ),
        (
            'Картинка для рецепта',
            {
                'classes': ['wide'],
                'fields': ['image'],
            },
        ),
        (
            'Автор рецепта',
            {
                'classes': ['wide'],
                'fields': ['author'],
            },
        ),
    ]

    @admin.action(description="Удалить название")
    def delete_title(self, request, queryset):
        queryset.update(title="")

    @admin.action(description="Удалить описание")
    def delete_description(self, request, queryset):
        queryset.update(description="")

    @admin.action(description="Удалить рецепт")
    def delete_cooking_steps(self, request, queryset):
        queryset.update(cooking_steps="")

    @admin.action(description="Удалить продукты")
    def delete_products(self, request, queryset):
        queryset.update(products="")

    @admin.action(description="Удалить картинку")
    def delete_image(self, request, queryset):
        queryset.update(image="")

    def about_image(self, obj):
        if obj.image:
            return 'YES picture'
        else:
            return 'NO picture'