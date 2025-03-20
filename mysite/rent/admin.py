from django.contrib import admin
from .models import Group, Product, Status, Reservation, Profile


class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0

class StatusAdmin(admin.ModelAdmin):
    list_display = ['product', 'uuid', 'customer', 'condition']
    list_filter = ['product', 'uuid', 'condition']
    search_fields = ['product__name', 'uuid', 'customer__username']
    list_editable = ['customer', 'condition']
    fieldsets = [
        ('General', {'fields': ['product']}),
        ('Availability', {'fields': ['customer','condition']}),
    ]
    inlines = [ReservationInline]

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
    list_display = ['status_uuid', 'customer', 'start_date', 'end_date']
    list_editable = ['customer', 'start_date', 'end_date']
    list_display_links = ['status_uuid']
    list_filter = ['customer', 'status__uuid']

    def status_uuid(self, obj):
        if obj.status and obj.status.uuid:
            return str(obj.status.uuid)[:6]
        return "No Status"

    status_uuid.short_description = "Status UUID"
    status_uuid.admin_order_field = 'status__uuid'


# Register your models here.
admin.site.register(Group)
admin.site.register(Product, ProductAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Profile)