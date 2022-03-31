from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='poke_search_home'),
    path('about/', views.about, name='poke_search_about'),
]