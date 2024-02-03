from django.db import models
from users.models import Users
from django.core.validators import MinValueValidator, \
                                   MinLengthValidator


app_label = 'recipe_book'


class Recipes(models.Model):
    title = models.CharField(validators=[MinLengthValidator(3)], max_length=50)
    description = models.TextField(max_length=1000)
    cooking_steps = models.TextField()
    products = models.TextField(blank=True, null=True)
    cooking_time_in_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='photos_cooked_recipes/', blank=True, null=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f'Recipes( ' \
               f'title: {self.title}, ' \
               f'author: {self.author.email}' \
               f' )'


class RecipeCategories(models.Model):
    title = models.CharField(validators=[MinLengthValidator(3)], max_length=100, unique=True)
    recipes = models.ManyToManyField(Recipes)

    def __str__(self):
        return f'{self.title}'
