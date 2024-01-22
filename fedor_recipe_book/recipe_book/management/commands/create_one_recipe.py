from users.models import Users
from recipe_book.models import Recipes
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create one recipe in db"

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='Title recipe')
        parser.add_argument('description', type=str, help='Description recipe')
        parser.add_argument('cooking steps', type=str, help='Cooking steps recipe')
        parser.add_argument('products', type=str, help='Products for recipe')
        parser.add_argument('cooking time in minutes', type=int, help='Cooking time in minutes')
        parser.add_argument('user id', type=int, help='Id author recipe')

    def handle(self, *args, **kwargs):

        title: str = kwargs.get('title')
        description: str = kwargs.get('description')
        cooking_steps: str = kwargs.get('cooking steps')
        products: str = kwargs.get('products')
        cooking_time_in_minutes: int = kwargs.get('cooking time in minutes')
        user_id: int = kwargs.get('user_id')

        user = Users.objects.get(user_id)

        answer = None

        if user:

            recipes = Recipes(
                author=user,
                title=title,
                products=
                products,
                description=
                description,
                cooking_steps=
                cooking_steps,
                cooking_time_in_minutes=
                cooking_time_in_minutes
            )

            recipes.save()
            answer = recipes

        self.stdout.write(str(answer))