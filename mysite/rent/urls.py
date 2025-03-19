from django.urls import path
from .views import index, products, product, search
from .import views
from django.urls import include


urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),
    path("product/<int:product_id>", product, name="product"),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path('profile/', views.profile, name='profile'),
    path('statuses/', views.StatusListView.as_view(), name='statuses'),
    path('statuses/<int:pk>', views.StatusDetailView.as_view(), name='single_status'),
    path('statuses/new/', views.StatusCreateView.as_view(), name='status_new'),
    path('myproducts/', views.CustomerProductsListView.as_view(), name='myproducts'),
]