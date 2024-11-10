from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_ingredient, name='add_ingredient'),
    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path(
        'ingredients/<slug:ingredient_slug>/',
        views.ingredient_detail,
        name='ingredient_detail'
    ),
    path(
        'ingredients/<slug:ingredient_slug>/edit/',
        views.ingredient_edit, name='ingredient_edit'
    ),
    path(
        'ingredients/<slug:ingredient_slug>/delete/',
        views.ingredient_delete, name='ingredient_delete'
    ),
    path(
        'add_amount_per_day/', views.add_amount_per_day,
        name='add_amount_per_day'
    ),
    path(
        'my_amount_per_day_list/', views.my_amount_per_day_list,
        name='my_amount_per_day_list'
    ),
]
