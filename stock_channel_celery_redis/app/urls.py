from django.urls import path
from . import views

urlpatterns = [
    path("stockpicker/", views.stockpicker, name="stockpicker"),
    path("stocktracker/", views.stocktracker, name="stocktracker"),
]
