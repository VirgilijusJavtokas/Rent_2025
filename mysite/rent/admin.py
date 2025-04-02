from django.contrib import admin
from .models import Group, Product, Status, Reservation, Profile


class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    fields = ('customer', 'status', 'start_date', 'end_date', 'is_approved')
    readonly_fields = ('customer', 'status', 'start_date', 'end_date')
    can_delete = False


class StatusAdmin(admin.ModelAdmin):
    list_display = ['product', 'uuid', 'condition']
    list_filter = ['product', 'uuid', 'condition']
    search_fields = ['product__name', 'uuid']
    list_editable = ['condition']
    fieldsets = [
        ('General', {'fields': ['product']}),
        ('Availability', {'fields': ['condition']}),
    ]
    inlines = [ReservationInline]


class StatusInline(admin.TabularInline):
    model = Status
    extra = 0
    fields = ('uuid', 'condition')
    readonly_fields = ('uuid',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'quantity', 'inv_no', 'status_condition']
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
    list_display = ['status_uuid', 'customer', 'start_date', 'end_date', 'is_approved']
    list_editable = ['customer', 'start_date', 'end_date', 'is_approved']
    list_display_links = ['status_uuid']
    list_filter = ['customer', 'status__uuid', 'is_approved']
    search_fields = ['status__uuid', 'customer__username']
    actions = ['approve_reservations', 'reject_reservations']

    def status_uuid(self, obj):
        if obj.status and obj.status.uuid:
            return str(obj.status.uuid)[:6]
        return "No Status"

    status_uuid.short_description = "Status UUID"
    status_uuid.admin_order_field = 'status__uuid'

    # Add bulk approval functionality
    def approve_reservations(self, request, queryset):
        """Sets reservations as approved."""
        count = queryset.update(is_approved=True)
        self.message_user(request, f"{count} rezervacija (-os) patvirtinta.")

    approve_reservations.short_description = "Patvirtinti pasirinktas rezervacijas"

    def reject_reservations(self, request, queryset):
        """Rejects reservations by deleting them."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} rezervacija (-os) atšaukta.")

    reject_reservations.short_description = "Atšaukti pasirinktas rezervacijas"


# Register your models here.
admin.site.register(Group)
admin.site.register(Product, ProductAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Profile)
