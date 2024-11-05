from django.contrib import admin

from .models import Ingredient, AmountPerDay

admin.site.register(Ingredient)
admin.site.register(AmountPerDay)
