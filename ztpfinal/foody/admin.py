from django.apps import apps
from django.contrib import admin

models = apps.get_models()

for model in models:
    admin.site.register(model)
