from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.loginP, name="login"),
    path('logout/', views.logoutU, name="logout"),
    path('register/', views.registerP, name="register"),
    path('nawyki/dodaj_nawyk/', views.dodajNawyk, name="dodaj_nawyk"),
    path('nawyki/edytuj_nawyk/<str:pk>/', views.edytujNawyk, name="edytuj_nawyk"),
    path('nawyki/usun_nawyk/<str:pk>/', views.usunNawyk, name="usun_nawyk"),
    path('nawyki/', views.nawyki, name="nawyki"),
    path('statystyki/', views.statystyki, name="stats"),
]
