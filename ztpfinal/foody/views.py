import json

from django.contrib import auth
from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse, HttpResponse

from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *


def unauthorized():
    return HttpResponse('Unauthorized', status=401)


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
            return unauthorized()


class IngredientFind(APIView):
    def get_object(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient)
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
                recipes = recipes.filter(ingredients=ingredient_id)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)



class RegisterView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


# TODO change to LoginView when making frontend
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return JsonResponse({'user': f'{username}'})
    else:
        return JsonResponse({'error': f'User {username} does not exist or incorrect password given'})


def logout(request):
    auth.logout(request)
    return JsonResponse({'msg': 'Logged out'})


class FavouritesList(APIView):
    def get(self, request):
        user_id = request.query_params.get('userid')
        user_favourites = AppUser.objects.get(original_user_id=user_id)
        serializer = AppUserSerializer(user_favourites)
        return Response(serializer.data)
    # TODO add POSTing to favourites (logged-in user only)
