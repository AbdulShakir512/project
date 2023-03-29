from django.contrib import admin
from django.apps import apps
# Register your models here.
polls_models = apps.get_app_config('polls').get_models()

for model in polls_models:
    admin.site.register(model)