from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_ini, name='base_ini'),
    path('home', views.base, name='base'),
    path('animal/<str:id_animal>/', views.animal_detail, name='animal_detail'),
    path('litière', views.litière, name='litière')
]
