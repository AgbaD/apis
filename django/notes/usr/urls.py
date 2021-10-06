from django.urls import path
from . import views

urlpatterns = [
    path('dash', views.dash, name='dash'),
    path('note/<str:public_id>/', views.get_note, name='note')
]
