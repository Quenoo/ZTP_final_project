"""ztpfinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views as auth_views

from foody import views


schema_view = get_schema_view(
    openapi.Info(
        title="Foody API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ingredients/<int:pk>/', views.IngredientFind.as_view()),
    path('recipes', views.RecipesList.as_view()),
    path('recipes/<int:pk>/', views.RecipesFind.as_view()),
    path('ingredients/', views.IngredientList.as_view()),
    path('recipe_ingredients/', views.RecipeIngredientList.as_view()),
    path('favourites', views.FavouritesList.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', auth_views.obtain_auth_token,),
    path('logout/', views.LogoutView.as_view()),
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0))
]
