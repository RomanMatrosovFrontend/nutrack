from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='index'),
        name='logout'
    ),
    path('login/', views.login_view, name='login'),
    path('<slug:username>/', views.profile_details, name='profile'),
]
