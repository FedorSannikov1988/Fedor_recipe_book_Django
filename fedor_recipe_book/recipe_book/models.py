from django.db import models
from django.core.validators import MinValueValidator


class Recipes(models.Model):
    title = models.CharField(min_length=3, max_length=50)
    description = models.TextField(max_length=1000)
    cooking_steps = models.TextField()
    products = models.TextField(blank=True, null=True)
    cooking_time_in_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='photos_cooked_recipes/', blank=True, null=True)
    #author = models.CharField(min_length=3, max_length=100, blank=True, null=True)


class RecipeCategories(models.Model):
    title = models.CharField(min_length=3, max_length=100)
    recipes = models.ManyToManyField(Recipes, on_delete=models.CASCADE)
