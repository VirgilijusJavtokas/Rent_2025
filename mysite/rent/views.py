from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Group, Product, Status, Reservation
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ReservationForm

def index(request):
    num_products = Product.objects.all().count()
    num_groups = Group.objects.all().count()
    num_status = Status.objects.all().count()
    num_users = User.objects.all().count()

    context = {
        'num_products': num_products,
        'num_status': num_status,
        'num_groups': num_groups,
        'num_users': num_users,
    }
    return render(request, 'base.html', context)

def products(request):
    all_products = Product.objects.all()

    lighting_products = all_products.filter(group__name="Apšvietimas")
    furniture_products = all_products.filter(group__name="Baldai")
    tent_products = all_products.filter(group__name="Palapinės")

    lighting_paginator = Paginator(lighting_products, 3)
    furniture_paginator = Paginator(furniture_products, 3)
    tent_paginator = Paginator(tent_products, 3)

    lighting_page_number = request.GET.get('lighting_page', 1)
    furniture_page_number = request.GET.get('furniture_page', 1)
    tent_page_number = request.GET.get('tent_page', 1)

    lighting_page = lighting_paginator.get_page(lighting_page_number)
    furniture_page = furniture_paginator.get_page(furniture_page_number)
    tent_page = tent_paginator.get_page(tent_page_number)

    context = {
        'lighting_page': lighting_page,
        'furniture_page': furniture_page,
        'tent_page': tent_page,
    }

    return render(request, 'products.html', context)


def product(request, product_id):
    context = {"product": Product.objects.prefetch_related('product_status').get(id=product_id)
}
    return render(request, 'product.html', context)

def search(request):
    query = request.GET.get('query')
    product_search_result = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(group__name__icontains=query))
    context = {
        'query': query,
        'products': product_search_result,
    }
    return render(request, 'search.html', context)


# @login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reservations = Reservation.objects.filter(product=product)

    if request.method == "POST":
        print("Gauta POST užklausa:", request.POST)  # Patikrinsime, ar duomenys ateina
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.product = product
            reservation.user = request.user
            reservation.save()
            return JsonResponse({'status': 'success', 'message': 'Rezervacija sukurta!'})  # AJAX grįžtamasis ryšys
        else:
            print("Forma neteisinga:", form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors})

    else:
        form = ReservationForm()

    return render(request, 'product.html', {
        'product': product,
        'reservations': reservations,
        'form': form,
    })


class CustomerProductsListView(LoginRequiredMixin, generic.ListView):
    model = Status
    template_name = "my_products.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Status.objects.filter(customer=self.request.user)
