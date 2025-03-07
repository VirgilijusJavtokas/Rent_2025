from django.contrib import admin
from .models import Group, Product, Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ['product', 'condition','due_date']
    list_filter = ['product', 'due_date']
    search_fields = ['product']

class StatusInline(admin.TabularInline):
    model = Status
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity','inv_no', 'status_condition']
    list_filter = ['name', 'inv_no']
    search_fields = ['name']
    inlines = [StatusInline]

    def status_condition(self, obj):
        status = Status.objects.filter(product=obj).first()
        if status:
            return status.get_condition_display()
        return "No Status"

    status_condition.short_description = 'Būsena'




# Register your models here.
admin.site.register(Group)
admin.site.register(Product, ProductAdmin)
admin.site.register(Status, StatusAdmin)