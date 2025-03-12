from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, Product, Status
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    num_products = Product.objects.all().count()
    num_status = Status.objects.all().count()
    num_groups = Group.objects.all().count()

    context = {
        'num_products': num_products,
        'num_status': num_status,
        'num_groups': num_groups,
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
    context = {"product": Product.objects.get(pk=product_id)}
    return render(request, 'product.html', context)

def search(request):
    query = request.GET.get('query')
    product_search_result = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(group__name__icontains=query))
    context = {
        'query': query,
        'products': product_search_result,
    }
    return render(request, 'search.html', context)