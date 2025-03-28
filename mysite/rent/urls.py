from django.urls import path
from .import views


urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.products, name="products"),
    path("product/<int:product_id>", views.product, name="product"),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path('profile/', views.profile, name='profile'),
    path('statuses/', views.StatusListView.as_view(), name='statuses'),
    path('statuses/<int:pk>', views.StatusDetailView.as_view(), name='single_status'),
    path('statuses/<int:pk>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('statuses/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
    path('statuses/new/', views.StatusCreateView.as_view(), name='status_new'),
    path('statuses/<int:pk>/new', views.ReservationCreateView.as_view(), name='reservation_new'),
    path('my-reservations/', views.ReservationListView.as_view(), name='my_reservations'),
    path('reservation/<int:status_pk>/<int:pk>/update/', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('reservation/<int:status_pk>/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),
    path('product/<int:product_id>/reserve/', views.reserve_product, name='reservation_new'),
    path('reservation/<int:status_pk>/<int:pk>/approve/', views.approve_reservation, name='reservation_approve'),
    path('product/<int:product_id>/statuses/', views.product_statuses, name='reservations_per_status'),
]