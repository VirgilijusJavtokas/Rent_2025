from django.contrib import admin
from .models import RentGroup, RentProduct, ProductInstance

# Register your models here.
admin.site.register(RentGroup)
admin.site.register(RentProduct)
admin.site.register(ProductInstance)