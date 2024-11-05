from django.shortcuts import render, redirect

from .forms import IngredientForm
from .models import Ingredient


def index(request):
    """Функция отображения главной страницы"""
    context = {
        'num_ingredients': Ingredient.objects.all().count()
    }
    return render(request, 'index.html', context,)


def add_ingredient(request):
    """Страница создания ингредиента"""
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            return redirect('ingredient_list')
        else:
            return render(request, 'add_ingredient.html', {'form': form})
    else:
        form = IngredientForm()
    return render(request, 'add_ingredient.html', {'form': form})
