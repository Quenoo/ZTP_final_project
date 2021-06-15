from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Ingredient, RecipeIngredient
from .models import Recipe
from .models import AppUser


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer

    class Meta:
        model = Recipe
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])

        app_user = AppUser.objects.create(user=user)
        app_user.favourite_recipes.set([])

        user.save()
        app_user.save()

        return user

