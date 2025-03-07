from django.urls import path
from .views import index, products, product
from .import views
from django.urls import include


urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),
    path("product/<int:product_id>", product, name="product"),
]