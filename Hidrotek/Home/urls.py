from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('services/', views.services, name='services'),
    path('category/<str:foo>', views.category, name='category'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]
