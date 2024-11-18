from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.views import custom_forbidden_view
from .forms import (
    CustomAuthenticationForm, CustomUserCreationForm,
    PasswordEditForm, ProfileEditForm,
)


User = get_user_model()


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def profile_details(request, username):
    user = get_object_or_404(User, username=username)
    ingredients = user.ingredient_set.all().count()
    amount_per_days = user.amountperday_set.all().count()
    return render(
        request, 'users/profile.html',
        {
            'profile': user, 'ingredients': ingredients,
            'amount_per_days': amount_per_days
        }
    )


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user and not request.user.is_superuser:
        return custom_forbidden_view(request)

    if request.method == 'POST':
        if (
            'email' in request.POST or
            'first_name' in request.POST or
            'last_name' in request.POST
        ):
            form = ProfileEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
                profile_form = form
                password_form = PasswordEditForm()
        if 'password1' in request.POST or 'password2' in request.POST:
            form = PasswordEditForm(instance=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Пароль успешно изменен')

            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
                profile_form = ProfileEditForm(instance=user)
                password_form = form

    profile_form = ProfileEditForm(instance=user)
    password_form = PasswordEditForm()
    return render(request, 'users/profile_edit.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'user': user
    })


def logout_view(request):
    logout(request)
    next_page = request.GET.get('next', 'index')
    return redirect(next_page)
