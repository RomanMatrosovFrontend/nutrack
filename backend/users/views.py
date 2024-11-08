from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})
