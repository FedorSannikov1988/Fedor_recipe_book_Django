from django.contrib import admin
from recipe_book.models import Recipes, \
                               RecipeCategories, \
                               CommentsOnRecipe


class RecipesAdmin(admin.ModelAdmin):
    list_display = ['title']
    #ordering = ['birthday']
    #list_filter = ['birthday']
    #search_fields = ['email']
    #search_help_text = 'Поиск по полю email'


admin.site.register(Recipes, RecipesAdmin)
admin.site.register(RecipeCategories)
admin.site.register(CommentsOnRecipe)
