from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from core.views import custom_forbidden_view

from .forms import (
    AmountPerDayForm, FilterAmountPerDayForm,
    FilterIngredientForm, IngredientForm
)
from .models import AmountPerDay, Ingredient
from .utils import (
    get_dynamics_of_changes, get_total_nutrients
)


def index(request):
    num_ingredients = cache.get('num_ingredients')
    if num_ingredients is None:
        num_ingredients = Ingredient.objects.count()
        cache.set('num_ingredients', num_ingredients, 300)
    context = {'num_ingredients': num_ingredients}
    return render(request, 'nutritional_value/index.html', context)


@login_required
def add_ingredient(request):
    """Страница создания ингредиента"""
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
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
    cache_key = (
        f'ingredients_list_{request.GET.get("search", "")}_author_'
        f'{form.cleaned_data.get("author", "") if form.is_valid() else ""}'
    )
    ingredients = cache.get(cache_key)
    if ingredients is None:
        ingredients = Ingredient.objects.select_related('author').all()
    if form.is_valid() and form.cleaned_data['author']:
        ingredients = ingredients.filter(author=form.cleaned_data['author'])
    query = request.GET.get('search')
    if query:
        ingredients = ingredients.filter(title__icontains=query)
    cache.set(cache_key, ingredients, 300)
    paginator = Paginator(ingredients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request, 'nutritional_value/ingredient_list.html',
        {'page_obj': page_obj, 'form': form}
    )


def ingredient_detail(request, ingredient_slug):
    ingredient = get_object_or_404(
        Ingredient.objects.select_related('author'), slug=ingredient_slug)
    return render(
        request, 'nutritional_value/ingredient_detail.html',
        {'ingredient': ingredient}
    )


@login_required
def ingredient_edit(request, ingredient_slug):
    ingredient = get_object_or_404(
        Ingredient.objects.select_related('author'), slug=ingredient_slug)
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
    ingredient = get_object_or_404(
        Ingredient.objects.select_related('author'), slug=ingredient_slug)
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
    amounts = AmountPerDay.objects.select_related(
        'ingredient', 'author').filter(author=request.user).order_by('date')
    context = {'form': form}
    dynamics_of_changes = None
    cut_size = 'day'
    if form.is_valid():
        if form.cleaned_data['date_start']:
            amounts = amounts.filter(date__gte=form.cleaned_data['date_start'])
        if form.cleaned_data['date_stop']:
            amounts = amounts.filter(date__lte=form.cleaned_data['date_stop'])
        cut_size = form.cleaned_data['cut_size']

    paginator = Paginator(amounts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    total = get_total_nutrients(amounts)
    dynamics_of_changes = get_dynamics_of_changes(cut_size, amounts)
    context['total_count'] = total['total_count']
    if context['total_count'] > 0:
        context['dynamics_of_changes'] = dynamics_of_changes
        context['cut_size'] = cut_size
        periods_count = len(dynamics_of_changes)
        context['average_calories'] = total['total_calories'] / periods_count
        context['average_proteins'] = total['total_proteins'] / periods_count
        context['average_fats'] = total['total_fats'] / periods_count
        context['average_carbohydrates'] = (
            total['total_carbohydrates'] /
            periods_count
        )

    return render(
        request, 'nutritional_value/my_amount_per_day_list.html', context
    )


@login_required
def amount_per_day_delete(request, id):
    amount_per_day = get_object_or_404(
        AmountPerDay.objects.select_related('author', 'ingredient'), id=id)
    if request.user != amount_per_day.author and not request.user.is_superuser:
        return custom_forbidden_view(request)
    if request.method == 'POST':
        amount_per_day.delete()
        return redirect('my_amount_per_day_list')

    return render(
        request, 'nutritional_value/amount_per_day_confirm_delete.html',
        {'amount_per_day': amount_per_day}
    )
