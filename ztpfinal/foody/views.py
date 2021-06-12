import json

from django.contrib import auth
from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *


class IngredientList(APIView):
    def get(self):
        """
        List all ingredients
        """
        snippets = Ingredient.objects.all()
        serializer = IngredientSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Add new ingredient
        """
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


# TODO change to LoginView when making frontend
@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return JsonResponse({'user': f'{username}'})
    else:
        return JsonResponse({'error': f'User {username} does not exist'})


def logout(request):
    auth.logout(request)
