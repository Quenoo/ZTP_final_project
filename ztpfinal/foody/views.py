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
        if request.user.is_authenticated:
            serializer = IngredientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return unauthorized()


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
