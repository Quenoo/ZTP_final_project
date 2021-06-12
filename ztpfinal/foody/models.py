from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)

    def __str__(self):
        return self.ingredient_name


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe_instructions = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_recipes = models.ManyToManyField(Recipe)
