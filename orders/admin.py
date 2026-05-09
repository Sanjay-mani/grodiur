from django.contrib import admin
from .models import Order, OrderItem, SupportTicket

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'display_user', 'full_name', 'status', 
                    'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'user__username', 'full_name', 'user__first_name', 'user__last_name']
    list_editable = ['status']
    inlines = [OrderItemInline]

    def display_user(self, obj):
        if obj.user.first_name:
            return f"{obj.user.first_name} {obj.user.last_name}".strip()
        if obj.user.username.isdigit():
            return obj.user.username
        return obj.user.email
    display_user.short_description = "Customer"

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'order', 'display_user', 'issue_type', 'status', 'created_at']
    list_filter = ['status', 'issue_type', 'created_at']
    search_fields = ['ticket_id', 'order__order_id', 'user__username', 'message']
    list_editable = ['status']
    readonly_fields = ['created_at', 'ticket_id']

    def display_user(self, obj):
        if obj.user.first_name:
            return f"{obj.user.first_name} {obj.user.last_name}".strip()
        if obj.user.username.isdigit():
            return obj.user.username
        return obj.user.email
    display_user.short_description = "User"