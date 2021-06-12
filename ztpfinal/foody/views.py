from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *


class IngredientList(APIView):
    def get(self, request, format=None):
        """
        List all ingredients
        """
        snippets = Ingredient.objects.all()
        serializer = IngredientSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Add new ingredient
        """
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
