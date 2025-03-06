from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, Product, Status

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