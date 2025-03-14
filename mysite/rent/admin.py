from django.contrib import admin
from .models import Group, Product, Status, Reservation


class StatusAdmin(admin.ModelAdmin):
    list_display = ['product', 'uuid', 'customer', 'condition', 'due_back']
    list_filter = ['product', 'uuid', 'condition']
    search_fields = ['product']
    list_editable = ['customer', 'condition', 'due_back']
    ordering = ['due_back']
    date_hierarchy = 'due_back'
    fieldsets = [
        ('General', {'fields': ['product', 'uuid']}),
        ('Availability', {'fields': ['customer','condition', 'due_back']}),
    ]


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

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['product', 'start_date', 'end_date']
    list_editable = ['start_date', 'end_date']
    fieldsets = [
        ('General', {'fields': ['product']}),
        ('Availability', {'fields': ['start_date', 'end_date']}),
    ]


# Register your models here.
admin.site.register(Group)
admin.site.register(Product, ProductAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Reservation, ReservationAdmin)