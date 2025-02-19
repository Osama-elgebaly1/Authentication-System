from django.urls import path
from .views import *

urlpatterns = [
    path('register/',register,name='register'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('change-password/',change_password,name='change_password'),
    path('profile/<int:pk>/',user_profile,name='profile'),
]
