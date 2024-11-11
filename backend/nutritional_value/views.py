from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import  F, Sum
from django.shortcuts import get_object_or_404, redirect, render

from core.views import custom_forbidden_view
from .forms import (
    AmountPerDayForm, FilterAmountPerDayForm,
    FilterIngredientForm, IngredientForm
)
from .models import AmountPerDay, Ingredient
from .utils import get_total_nutrients


def index(request):
    """Функция отображения главной страницы"""
    context = {
        'num_ingredients': Ingredient.objects.all().count(),
        'user': request.user
    }
    return render(request, 'nutritional_value/index.html', context,)


@login_required
def add_ingredient(request):
    """Страница создания ингредиента"""
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            ingredient = form.save()
            return redirect('ingredient_list')
        else:
            return render(
                request, 'nutritional_value/add_ingredient.html',
                {'form': form}
            )
    else:
        form = IngredientForm()
    return render(
        request, 'nutritional_value/add_ingredient.html',
        {'form': form}
    )


def ingredient_list(request):
    form = FilterIngredientForm(request.GET or None)
    ingredients = Ingredient.objects.all()
    if form.is_valid() and form.cleaned_data['author']:
        ingredients = ingredients.filter(author=form.cleaned_data['author'])
    query = request.GET.get('search')
    if query:
        ingredients = ingredients.filter(title__icontains=query)
    paginator = Paginator(ingredients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request, 'nutritional_value/ingredient_list.html',
        {'page_obj': page_obj, 'form': form}
    )


def ingredient_detail(request, ingredient_slug):
    ingredient = get_object_or_404(Ingredient, slug=ingredient_slug)
    return render(
        request, 'nutritional_value/ingredient_detail.html',
        {'ingredient': ingredient}
    )


@login_required
def ingredient_edit(request, ingredient_slug):
    ingredient = get_object_or_404(Ingredient, slug=ingredient_slug)
    if request.user != ingredient.author and not request.user.is_superuser:
        return custom_forbidden_view(request)
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
        request, 'nutritional_value/ingredient_edit.html',
        {'form': form, 'ingredient': ingredient}
    )


@login_required
def ingredient_delete(request, ingredient_slug):
    ingredient = get_object_or_404(Ingredient, slug=ingredient_slug)
    if request.user != ingredient.author and not request.user.is_superuser:
        return custom_forbidden_view(request)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredient_list')

    return render(
        request, 'nutritional_value/ingredient_confirm_delete.html',
        {'ingredient': ingredient}
    )


@login_required
def add_amount_per_day(request):
    if request.method == 'POST':
        form = AmountPerDayForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('my_amount_per_day_list')
        else:
            return render(
                request, 'nutritional_value/add_amount_per_day.html',
                {'form': form}
            )
    else:
        form = AmountPerDayForm()
    return render(
        request, 'nutritional_value/add_amount_per_day.html',
        {'form': form}
    )


@login_required
def my_amount_per_day_list(request):
    form = FilterAmountPerDayForm(request.GET or None)
    amounts = AmountPerDay.objects.filter(author=request.user).order_by('date')
    if form.is_valid() and form.cleaned_data['date']:
        amounts = amounts.filter(date=form.cleaned_data['date'])
    paginator = Paginator(amounts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_nutrients = get_total_nutrients(amounts)

    return render(
        request, 'nutritional_value/my_amount_per_day_list.html',
        {
            'page_obj': page_obj, 'form': form,
            'total_nutrients': total_nutrients
        }
    )


@login_required
def amount_per_day_delete(request, id):
    amount_per_day = get_object_or_404(AmountPerDay, id=id)
    if request.user != amount_per_day.author and not request.user.is_superuser:
        return custom_forbidden_view(request)
    if request.method == 'POST':
        amount_per_day.delete()
        return redirect('my_amount_per_day_list')

    return render(
        request, 'nutritional_value/amount_per_day_confirm_delete.html',
        {'amount_per_day': amount_per_day}
    )
