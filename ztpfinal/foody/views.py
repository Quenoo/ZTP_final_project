from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *


class IngredientList(APIView):
    def get(self, request):
        """
        List all ingredients
        """
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Add new ingredient
        """
        if request.user.is_authenticated:
            serializer = IngredientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied


class IngredientFind(APIView):
    def get_object(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise NotFound

    def get(self, request, pk, format=None):
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        ingredient = self.get_object(pk)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeIngredientList(APIView):
    def get(self, request):
        """
        List all recipe ingredients
        """
        recipe_ingredients = RecipeIngredient.objects.all()
        serializer = RecipeIngredientSerializer(recipe_ingredients, many=True)
        return Response(serializer.data)


class RecipesList(APIView):
    def get(self, request, format=None):
        """
        List all recipes or containing chosen ingredients
        """
        ingredient_list = request.query_params.get('ingredients')
        recipes = Recipe.objects.all()
        if ingredient_list:
            ingredient_list = list(map(int, ingredient_list.split(',')))
            recipes = Recipe.objects.all()
            for ingredient_id in ingredient_list:
                ingredient = Ingredient.objects.get(id=ingredient_id)
                recipes = recipes.filter(ingredients=ingredient)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

class RecipesFind(APIView):
    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        recipe = self.get_object(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavouritesList(APIView):
    def get(self, request):
        user_id = request.query_params.get('userid')
        user = User.objects.get(id=user_id)
        user_favourites = AppUser.objects.get(user=user).favourite_recipes.all()
        serializer = RecipeSerializer(user_favourites, many=True)
        return Response(serializer.data)
    # TODO add POSTing to favourites (logged-in user only)

    def post(self, request):
        try:
            new_fauvorite_recipe_id = request.data["recipeid"]
        except:
            return Response("Recipeid in body is required", status=status.HTTP_400_BAD_REQUEST)

        appuser_user = User.objects.get(username=request.user)
        appuser = AppUser.objects.get(user=appuser_user)
        new_fauvorite_recipe = Recipe.objects.get(pk=new_fauvorite_recipe_id)
        appuser.favourite_recipes.add(new_fauvorite_recipe)
        return Response(status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
