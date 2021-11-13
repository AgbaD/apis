from django.urls import path
from .views import Register, Login, Profile

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('profile/', Profile.as_view()),

]
