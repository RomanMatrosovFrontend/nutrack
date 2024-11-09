from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CustomAuthenticationForm, CustomUserCreationForm,
    EmailEditForm, PasswordEditForm,
)


User = get_user_model()


def custom_forbidden_view(request, error_message='Нет прав для доступа'):
    return render(
        request, 'common/403.html',
        status=403, context={'error_message': error_message}
    )


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
    return render(
        request, 'users/profile.html',
        {'user': user}
    )


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user and not request.user.is_superuser:
        return custom_forbidden_view(request)
    if request.method == 'POST':
        if 'email' in request.POST:
            form = EmailEditForm(instance=user, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('profile', username=username)
        elif 'password' in request.POST:
            form = PasswordEditForm(instance=user, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
    else:
        email_form = EmailEditForm(instance=user)
        password_form = PasswordEditForm()

    return render(request, 'users/profile_edit.html', {
        'email_form': email_form,
        'password_form': password_form,
        'user': user
    })
