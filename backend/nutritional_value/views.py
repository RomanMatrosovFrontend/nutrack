from django.shortcuts import render

from .models import Ingredient


def index(request):
    """Функция отображения главной страницы"""
    context = {
        'num_ingredients': Ingredient.objects.all().count()
    }
    return render(request, 'index.html', context,)
