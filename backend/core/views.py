from django.shortcuts import render


def custom_forbidden_view(request, error_message='Нет прав для доступа'):
    return render(
        request, 'common/403.html',
        status=403, context={'error_message': error_message}
    )
