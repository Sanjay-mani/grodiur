from django.contrib import admin
from .models import Coupon, Cart, CartItem

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'amount', 'min_order_value', 'is_active', 'expiry_date')
    list_filter = ('is_active', 'discount_type')
    search_fields = ('code',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
