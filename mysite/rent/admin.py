from django.contrib import admin
from .models import Group, Product, Status

# Register your models here.
admin.site.register(Group)
admin.site.register(Product)
admin.site.register(Status)