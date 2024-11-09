from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CustomAuthenticationForm, CustomUserCreationForm,
    EmailEditForm, PasswordEditForm,
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


def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
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
        email_form = EmailEditForm(instance=request.user)
        password_form = PasswordEditForm()

    return render(request, 'users/profile_edit.html', {
        'email_form': email_form,
        'password_form': password_form,
    })
