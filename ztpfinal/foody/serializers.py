from rest_framework import serializers

from .models import Ingredient
from .models import Recipe
from .models import AppUser


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('ingredient_name',)


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('recipe_name', 'author', 'recipe_instructions', 'ingredients')


class AppUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = ('user', 'favourite_recipes')
