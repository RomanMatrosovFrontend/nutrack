from django.urls import path

from . import views


urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
    path('login/', views.login_view, name='login'),
    path('<slug:username>/', views.profile_details, name='profile'),
    path('<slug:username>/edit/', views.edit_profile, name='edit_profile'),
]
