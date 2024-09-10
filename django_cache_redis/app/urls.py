from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r"countries", CountryViewSet, basename="countries")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", home, name="home"),
    path("cached", cached, name="cached"),
    path("cacheless", cacheless, name="cacheless"),
]
