from django.urls import path
from .views import index, products
from .import views
from django.urls import include


urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),
]