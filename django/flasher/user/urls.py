from django.urls import path
from . import views

urlpatterns = [
    path('page', views.page, name='page'),
    path('create_note', views.create_note, name='create_note')
]
