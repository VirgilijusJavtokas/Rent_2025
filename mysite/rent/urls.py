from django.urls import path
from .views import index
from .import views
from django.urls import include

urlpatterns = [
    path("", index, name="index"),
]