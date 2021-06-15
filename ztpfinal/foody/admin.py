from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Ingredient, RecipeIngredient
from .models import Recipe
from .models import AppUser


class AppUserInline(admin.StackedInline):
    model = AppUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (AppUserInline,)


# FIXME: For some reason, the recipe ingredients in the admin panel are only visible and editable
#  from the Recipes panel (sometimes visible from Ingredients). Seems to work fine in other places,
#  e.g. requests return recipe ingredients set with the new model.
#  Reference: https://docs.djangoproject.com/en/3.2/ref/contrib/admin/ 'Working with many-to-many intermediary models'
#  (same case)
#  Workaround for now: RecipeIngredientAdmin
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    inline = (RecipeIngredientInline,)


class RecipeAdmin(admin.ModelAdmin):
    inline = (RecipeIngredientInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
