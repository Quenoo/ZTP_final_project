from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)

    def __str__(self):
        return self.ingredient_name


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe_instructions = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def __str__(self):
        return self.recipe_name


class RecipeIngredient(models.Model):
    # units
    GRAMS = 'g'
    KILOGRAMS = 'kg'
    MILLILITRES = 'ml'
    LITRES = 'l'
    TEASPOONS = 'tsp'
    TABLESPOONS = 'tbsp'
    CUPS = 'cup'
    SLICES = 'sl'

    UNIT_CHOICES = [
        (GRAMS, 'grams'),
        (KILOGRAMS, 'kilograms'),
        (MILLILITRES, 'millilitres'),
        (LITRES, 'litres'),
        (TEASPOONS, 'teaspoons'),
        (TABLESPOONS, 'tablespoons'),
        (CUPS, 'cups'),
        (SLICES, 'slices')
    ]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(
        max_length=4,
        choices=UNIT_CHOICES,
        default=GRAMS,
    )

    def __str__(self):
        return f'Recipe({self.recipe.id})-Ingredient({self.ingredient.ingredient_name})-{self.amount}-{self.unit}'


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.user.username
