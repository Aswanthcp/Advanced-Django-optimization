from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from .models import Country
from .serializers import CountrySerializer
from datetime import datetime
import pytz
from rest_framework.decorators import action
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.utils.decorators import method_decorator
from rest_framework_extensions.cache.decorators import cache_response


def home(request):
    return render(request, "general/home.html")


@cache_page(60 * 15)
def cached(request):
    usermodel = get_user_model()
    all_users = usermodel.objects.all()
    return HttpResponse(
        "<html><body> <h1> {0} users... cashed</h1> </body></html>".format(
            len(all_users)
        )
    )


def cacheless(request):
    usermodel = get_user_model()
    all_users = usermodel.objects.all()
    return HttpResponse(
        "<html><body> <h1> {0} users... cashed</h1> </body></html>".format(
            len(all_users)
        )
    )


# Rest api ........................


class CountryViewSet1(viewsets.ViewSet):
    cache_key = "countries_with_time"

    def list(self, request):
        cached_data = cache.get(self.cache_key)
        if cached_data is None:

            countries = Country.objects.all()
            serializer = CountrySerializer(countries, many=True)

            current_time = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
            data = {"countries": serializer.data, "time": current_time}

            cache.set(self.cache_key, data, timeout=60 * 15)

            return Response(data)
        return Response(cached_data)

    def create(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Clear cache after adding a new country to ensure fresh data on the next list request
            cache.delete(self.cache_key)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CountryViewSet2(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        countries = self.get_queryset()
        serializer = CountrySerializer(countries, many=True)
        data = {
            "countries": serializer.data,
        }
        return Response(data)

    def create(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Clear cache after adding a new country to ensure fresh data on the next list request
            cache.delete(self.cache_key)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


CACHE_TTL = 60 * 15  # 15 minutes cache TTL


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    @cache_response(timeout=CACHE_TTL)
    def list(self, request, *args, **kwargs):
        """
        Lists all countries and caches the response for 15 minutes.
        """
        countries = self.get_queryset()  # Fetch all countries from the database
        serializer = CountrySerializer(countries, many=True)
        data = {
            "countries": serializer.data,
        }
        return Response(data)

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create method to invalidate the cache.
        """
        response = super().create(request, *args, **kwargs)
        cache.delete(CACHE_KEY)  # Clear the cache after a new country is created
        return response

    def update(self, request, *args, **kwargs):
        """
        Overrides the default update method to invalidate the cache.
        """
        response = super().update(request, *args, **kwargs)
        cache.delete(CACHE_KEY)  # Clear the cache after a country is updated
        return response

    def destroy(self, request, *args, **kwargs):
        """
        Overrides the default destroy method to invalidate the cache.
        """
        response = super().destroy(request, *args, **kwargs)
        cache.delete(CACHE_KEY)  # Clear the cache after a country is deleted
        return response
