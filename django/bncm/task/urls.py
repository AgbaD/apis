from django.urls import path
from .views import pu, lg, party

urlpatterns = [
    path("", pu, name="pu"),
    path("lga/", lg, name="lg"),
    path("party/", party, name="party")
]
