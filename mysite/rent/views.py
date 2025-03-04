from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, Product, Status

def index(request):
    num_products = Product.objects.count()
    num_status = Status.objects.count()
    num_groups = Group.objects.count()
    context = {
        'num_products': num_products,
        'num_status': num_status,
        'num_groups': num_groups,
    }
    return render(request, 'index.html', context)