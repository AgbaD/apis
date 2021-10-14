from rest_framework.authtoken import views as rest_views
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view()),
    path('login/', rest_views.obtain_auth_token),
    path('update_password/', views.UpdatePassword.as_view()),
    path('forgot_password/', views.ForgotPassword.as_view()),
    path('change_password/<str:payload>/', views.ChangePasswordFromForgot.as_view()),
    path('movie/all/', views.AllMovies.as_view()),
    path('movie/<int:pk>/', views.GetMovie.as_view()),
    path('movie/create/', views.CreateMovie.as_view()),
    path('movie/<int:pk>/edit/', views.MovieView.as_view()),
]
