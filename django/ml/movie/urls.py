from django.urls import path
from . import views

urlpatterns = [
    path('movie/<int:pk>/', views.movie, name='movie'),
    path('movies/', views.movies, name='movies'),
    path('register/', views.register, name='register'),
    path('login/', views.obtain_auth_token)
]
