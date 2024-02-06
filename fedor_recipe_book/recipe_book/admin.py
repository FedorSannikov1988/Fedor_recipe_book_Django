from django.contrib import admin
from recipe_book.models import Recipes, \
                               RecipeCategories, \
                               CommentsOnRecipe

admin.site.register(Recipes)
admin.site.register(RecipeCategories)
admin.site.register(CommentsOnRecipe)
