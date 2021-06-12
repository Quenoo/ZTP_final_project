from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Ingredient
from .models import Recipe
from .models import AppUser


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"#('pk', 'ingredient_name')#'__all__'#('pk', 'ingredient_name')


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"#('recipe_name', 'author', 'recipe_instructions')#, 'ingredients')


class AppUserSerializer(serializers.ModelSerializer):
    favourite_recipes = RecipeSerializer(read_only=True, many=True, )

    class Meta:
        model = AppUser
        fields = "__all__"#('user', 'favourite_recipes')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        app_user = AppUser.objects.create(user=user, original_user_id=user.id)
        user.set_password(validated_data['password'])
        app_user.favourite_recipes.set([])
        user.save()
        app_user.save()

        return user

