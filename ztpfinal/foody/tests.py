import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient

from foody.models import Ingredient, Recipe, RecipeIngredient, AppUser
from foody.serializers import UserSerializer
from foody.views import IngredientList


class TestIngredient(TestCase):
    def create_ingredient(self):
        ingredient = Ingredient.objects.create(ingredient_name='test_ingredient')
        return ingredient

    def test_ingredient(self):
        self.assertEqual(str(self.create_ingredient()), 'test_ingredient')


class TestRecipe(TestCase):
    def create_recipe(self):
        recipe = Recipe.objects.create(
            recipe_name='test_recipe',
            author=User.objects.create(username='test_author', password='test_password'),
            recipe_instructions='test_instructions'
        )
        return recipe

    def test_recipe(self):
        recipe = self.create_recipe()
        self.assertEqual(str(recipe), 'test_recipe')


class TestRecipeIngredient(TestCase):
    def test_recipe_ingredient(self):
        test_recipe_object = TestRecipe()
        test_recipe = test_recipe_object.create_recipe()
        test_ingredient_object = TestIngredient()
        test_ingredient = test_ingredient_object.create_ingredient()

        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=test_recipe,
            ingredient=test_ingredient,
            amount=100,
            unit='g'
        )
        self.assertEqual(str(recipe_ingredient), 'Recipe(1)-Ingredient(test_ingredient)-100-g')


class TestAppUser(TestCase):
    def test_app_user(self):
        user = User.objects.create(username='test_user', password='test_password')
        app_user = AppUser.objects.create(user=user)
        self.assertEqual(str(app_user), 'test_user')


class TestUserSerializer(TestCase):
    def test_user_serializer(self):
        validated_data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        serializer = UserSerializer()
        user = serializer.create(validated_data=validated_data)
        self.assertEqual(str(user), 'test_user')


class TestIngredientList(TestCase):
    def test_ingredient_list_post(self):
        User.objects.create_superuser(username='test_user')
        token = Token.objects.get(user__username='test_user')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client.post('/ingredients/', {'ingredient_name': 'test_ingredient'}, format='json')

        self.assertEqual(Ingredient.objects.count(), 1)

    def test_ingredient_list_post_bad_request(self):
        User.objects.create_superuser(username='test_user')
        token = Token.objects.get(user__username='test_user')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client.post('/ingredients/', {'wrong_field_name': 'test_ingredient'}, format='json')

        self.assertEqual(Ingredient.objects.count(), 0)

    def test_ingredient_list_get(self):
        client = APIClient()

        response = client.get('/ingredients/')

        self.assertEqual(response.status_code, 200)


class TestIngredientFind(TestCase):
    def test_ingredient_find(self):
        client = APIClient()

        Ingredient.objects.create(ingredient_name='test_ingredient')

        existing_ingredient = client.get('/ingredients/1/')
        non_existing_ingredient = client.get('/ingredients/2/')

        self.assertEqual(existing_ingredient.status_code, 200)
        self.assertEqual(non_existing_ingredient.status_code, 404)

    def test_ingredient_delete(self):
        Ingredient.objects.create(ingredient_name='test_ingredient')

        User.objects.create_superuser(username='test_user')
        token = Token.objects.get(user__username='test_user')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client.delete('/ingredients/1/')

        self.assertEqual(Ingredient.objects.count(), 0)


class TestRecipeIngredientList(TestCase):
    def test_recipe_ingredient_list_get(self):
        client = APIClient()

        response = client.get('/recipe_ingredients/')

        self.assertEqual(response.status_code, 200)


class TestRecipesList(TestCase):
    def test_recipes_list_get(self):
        Recipe.objects.create(
            recipe_name='test_recipe',
            author=User.objects.create(username='test_author', password='test_password'),
            recipe_instructions='test_instructions'
        )

        client = APIClient()

        response = client.get('/recipes')

        self.assertEqual(Recipe.objects.count(), 1)

    def test_recipes_list_get_params(self):
        recipe = Recipe.objects.create(
            recipe_name='test_recipe',
            author=User.objects.create(username='test_author', password='test_password'),
            recipe_instructions='test_instructions'
        )

        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=Ingredient.objects.create(ingredient_name='test_ingredient'),
            amount=100,
            unit='g'
        )

        client = APIClient()

        response = client.get('/recipes?ingredients=1')

        self.assertEqual(response.status_code, 200)

    def test_recipes_post(self):
        User.objects.create_user(username='test_user')
        token = Token.objects.get(user__username='test_user')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        Ingredient.objects.create(ingredient_name='post_test_ingredient')

        response = client.post('/recipes',
                               {
                                   'recipe_name': 'post_test_recipe',
                                   'recipe_instructions': 'post_test_instructions',
                                   'ingredients': []
                               }, format='json')

        self.assertEqual(Recipe.objects.count(), 1)


class TestRecipesFind(TestCase):
    def test_recipes_find(self):
        client = APIClient()

        Recipe.objects.create(
            recipe_name='test_recipe',
            author=User.objects.create(username='test_author', password='test_password'),
            recipe_instructions='test_instructions'
        )

        existing_recipe = client.get('/recipes/1/')
        non_existing_recipe = client.get('/recipes/2/')

        self.assertEqual(existing_recipe.status_code, 200)
        self.assertEqual(non_existing_recipe.status_code, 404)

    def test_recipe_delete(self):
        Recipe.objects.create(
            recipe_name='test_recipe',
            author=User.objects.create(username='test_author', password='test_password'),
            recipe_instructions='test_instructions'
        )

        User.objects.create_superuser(username='test_user')
        token = Token.objects.get(user__username='test_user')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client.delete('/recipes/1/')

        self.assertEqual(Recipe.objects.count(), 0)


class TestFavouritesList(TestCase):
    def test_favourites_list_post(self):
        Recipe.objects.create(
            recipe_name='test_recipe',
            author=User.objects.create(username='test_author', password='test_password'),
            recipe_instructions='test_instructions'
        )

        user = User.objects.create(username='test_user')
        app_user = AppUser.objects.create(user=user)
        token = Token.objects.get(user__username='test_user')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client.post('/favourites', {'recipe_id': 1}, format='json')

        self.assertEqual(app_user.favourite_recipes.all().count(), 1)
