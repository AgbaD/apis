from django.urls import path
from . import views

urlpatterns = [
    path('dash', views.dash, name='dash'),
    path('personal_notes', views.get_private_notes, name='get_private_notes'),
    path('create_note', views.create_note, name='create_note'),
    path('delete_note/<str:public_id>/', views.delete_note, name='delete_note'),
    path('get_note/<str:public_id>/', views.get_note, name='get_note')
]
