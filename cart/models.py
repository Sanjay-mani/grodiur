from django.db import models
from django.conf import settings
from products.models import Product

class Coupon(models.Model):
    DISCOUNT_TYPES = (
        ('flat', 'Flat Amount'),
        ('percent', 'Percentage'),
    )
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def get_total_mrp(self):
        return sum(item.get_mrp_subtotal() for item in self.items.filter(quantity__gt=0))

    def get_item_total(self):
        return sum(item.get_subtotal() for item in self.items.filter(quantity__gt=0))
        
    def get_discount(self):
        return self.get_total_mrp() - self.get_item_total()

    def get_coupon_discount(self):
        if not self.coupon:
            return 0
        item_total = self.get_item_total()
        if item_total < self.coupon.min_order_value:
            return 0
        if self.coupon.discount_type == 'flat':
            return min(self.coupon.amount, item_total)
        else:
            from decimal import Decimal
            return (self.coupon.amount / Decimal('100')) * item_total

    def get_delivery_fee(self):
        if self.get_item_total() >= 199:
            return 0
        return 1

    def get_final_total(self):
        return self.get_item_total() - self.get_coupon_discount() + self.get_delivery_fee()

    def get_total_items(self):
        return sum(item.quantity for item in self.items.filter(quantity__gt=0))
        
    def get_total_products(self):
        return self.items.filter(quantity__gt=0).count()

    def amount_needed_for_free_delivery(self):
        total = self.get_item_total()
        if total >= 199:
            return 0
        return 199 - total

    def get_total_savings(self):
        return self.get_discount() + self.get_coupon_discount()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.product.price * self.quantity

    def get_mrp_subtotal(self):
        mrp = self.product.mrp_price if self.product.mrp_price else self.product.price
        return mrp * self.quantity