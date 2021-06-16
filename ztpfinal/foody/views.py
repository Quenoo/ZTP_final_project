from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *
from .errors import *


class IngredientList(APIView):
    @swagger_auto_schema(operation_description="List all ingredients",
                         responses={200: "List of all ingredients"})
    def get(self, request):
        """
        List all ingredients
        :return: List of all ingredients
        """
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Add new ingredient (possible only for `staff_member`, i.e. moderator",
                         responses={200: "if valid",
                                    400: "if bad request"})
    @method_decorator(staff_member_required)
    def post(self, request):
        """
        Add new ingredient (possible only for `staff_member`, i.e. moderator)
        :return: 201 if valid, 400 otherwise
        """
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientFind(APIView):
    def get_object(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise NoModelWithAtrubute("Ingredient", "pk", pk)

    @swagger_auto_schema(operation_description="Get single ingredient",
                         responses={200: "if found",
                                    404: "if not found"})
    def get(self, request, pk, format=None):
        """
        Get single ingredient
        :param pk: ID of the ingredient
        :return: Ingredient if found for given ID, 404 otherwise
        """
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Delete an ingredient (possible only for `staff_member`, i.e. moderator)",
                         responses={204: "if no error"})
    @method_decorator(staff_member_required)
    def delete(self, request, pk, format=None):
        """
        Delete an ingredient (possible only for `staff_member`, i.e. moderator)
        :param pk: ID of the ingredient to remove
        :return: 204 if no error
        """
        ingredient = self.get_object(pk)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeIngredientList(APIView):
    @swagger_auto_schema(operation_description="List all ingredients (for all recipes)",
                         responses={200: "List of recipe ingredients"})
    def get(self, request):
        """
        List all ingredients (for all recipes)
        :return: List of recipe ingredients
        """
        recipe_ingredients = RecipeIngredient.objects.all()
        serializer = RecipeIngredientSerializer(recipe_ingredients, many=True)
        return Response(serializer.data)


class RecipesList(APIView):
    @swagger_auto_schema(operation_description="List all recipes (if no `ingredients=...` in query) "
                                               "or containing given ingredients (if `ingredients=...` present)",
                         responses={200: "A list of either all recipes or ones with given ingredients"})
    def get(self, request, format=None):
        """
        List all recipes (if no `ingredients=...` in query) or containing given ingredients (if `ingredients=...` present)
        :param request: recipes?ingredients=1,2,3,...
        :return: A list of either all recipes or ones with given ingredients
        """
        ingredient_list = request.query_params.get('ingredients')
        recipes = Recipe.objects.all()
        if ingredient_list:
            try:
                ingredient_list = list(map(int, ingredient_list.split(',')))
            except ValueError:
                ingredient_list = []

            recipes = Recipe.objects.all()
            for ingredient_id in ingredient_list:
                ingredient = Ingredient.objects.get(id=ingredient_id)
                recipes = recipes.filter(ingredients=ingredient)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Add new recipe (possible for all users)",
                         responses={201: "if valid",
                                    400: "if error"})
    @method_decorator(login_required)
    def post(self, request):
        """
        Add new recipe (possible for all users)
        :return: 201 if valid, 400 otherwise
        """
        try:
            request.data['author']
        except KeyError:
            request.data['author'] = request.user.id

        recipe_serializer = RecipeSerializer(data=request.data)
        if recipe_serializer.is_valid():
            recipe = recipe_serializer.save()

        try:
            recipe_ingredients = request.data['ingredients']
        except KeyError:
            raise NoModelWithAtrubute('ingredients')

        for recipe_ingredient_data in recipe_ingredients:
            recipe_ingredient_data['recipe'] = recipe.id

        recipe_ingredient_serializer = RecipeIngredientSerializer(data=recipe_ingredients, many=True)
        if recipe_ingredient_serializer.is_valid():
            recipe_ingredient_serializer.save()
            return Response(recipe_ingredient_serializer.data, status=status.HTTP_201_CREATED)

        return Response(recipe_ingredient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipesFind(APIView):
    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise NoModelWithAtrubute("Recipe", "pk", pk)

    @swagger_auto_schema(operation_description="Get single recipe",
                         responses={200: "Recipe if found for given ID, 404 otherwise"})
    def get(self, request, pk, format=None):
        """
        Get single recipe
        :param pk: ID of the recipe
        :return: Recipe if found for given ID, 404 otherwise
        """
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Delete a recipe (possible only for the recipe's author "
                                               "or a `staff_member`, i.e. moderator)",
                         responses={204: "if no error",
                                    403: "if forbidden"})
    @method_decorator(login_required)
    def delete(self, request, pk, format=None):
        """
        Delete a recipe (possible only for the recipe's author or a `staff_member`, i.e. moderator)
        :param pk: ID of the recipe to remove
        :return: 204 if no error, 403 if forbidden, 400 if there is no recipe with gicen id
        """
        recipe = self.get_object(pk)
        if not (request.user == recipe.author or request.user.is_staff_member):
            raise PermissionDenied
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavouritesList(APIView):
    @swagger_auto_schema(operation_description="Get favourite recipes for a user with given `user_id`",
                         responses={200: "Favourite recipes or empty list"})
    def get(self, request):
        """
        Get favourite recipes for a user with given `user_id`
        :param request: favourites?user_id=1
        :return: Favourite recipes or empty list
        """
        user_id = request.query_params.get('user_id')
        user = User.objects.get(id=user_id)
        user_favourites = AppUser.objects.get(user=user).favourite_recipes.all()
        serializer = RecipeSerializer(user_favourites, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Add a favourite recipe (given `recipe_id`) for user sending this"
                                               " request",
                         responses={200: "if no error",
                                    400: "if no recipe_id in request"})
    @method_decorator(login_required)
    def post(self, request):
        """
        Add a favourite recipe (given `recipe_id`) for user sending this request
        :param request: { "recipe_id": 1 }
        :return: 200 if no error, 400 if no recipe_id in request
        """
        try:
            new_favourite_recipe_id = request.data["recipe_id"]
        except KeyError:
            raise NoFieldInBody("recipe_id")


        app_user_user = User.objects.get(username=request.user)
        app_user = AppUser.objects.get(user=app_user_user)
        try:
            new_favourite_recipe = Recipe.objects.get(pk=new_favourite_recipe_id)
        except Recipe.DoesNotExist:
            raise NoModelWithAtrubute("Recipe", "pk", new_favourite_recipe_id)
        app_user.favourite_recipes.add(new_favourite_recipe)
        return Response(status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    """
    Register user (see README)
    """
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class LogoutView(APIView):
    @swagger_auto_schema(operation_description="Logout the current user, i.e. remove his token from the database",
                         responses={200: "if no error"})
    @method_decorator(login_required)
    def get(self, request, format=None):
        """
        Logout the current user, i.e. remove his token from the database
        :return: 200 if no error
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# For returning an error on @login_required redirect
class ForbiddenView(APIView):
    @swagger_auto_schema(operation_description="For returning an error on @login_required redirect")
    def get(self, request):
        """
        For returning an error on @login_required redirect
        """
        raise PermissionDenied
