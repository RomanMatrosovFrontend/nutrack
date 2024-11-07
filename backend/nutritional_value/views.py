from django.shortcuts import get_object_or_404, render, redirect

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


def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient_list.html', {'ingredients': ingredients})


def ingredient_detail(request, ingredient_slug):
    ingredient = get_object_or_404(Ingredient, slug=ingredient_slug)
    return render(request, 'ingredient_detail.html', {'ingredient': ingredient})


def ingredient_edit(request, ingredient_slug):
    ingredient = get_object_or_404(Ingredient, slug=ingredient_slug)

    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect(
                'ingredient_detail', ingredient_slug=ingredient.slug
            )
    else:
        form = IngredientForm(instance=ingredient)

    return render(
        request, 'ingredient_edit.html',
        {'form': form, 'ingredient': ingredient}
    )


def ingredient_delete(request, ingredient_slug):
    ingredient = get_object_or_404(Ingredient, slug=ingredient_slug)

    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredient_list')

    return render(
        request, 'ingredient_confirm_delete.html', {'ingredient': ingredient}
    )
