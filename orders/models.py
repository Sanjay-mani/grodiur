from django.db import models
from django.conf import settings
from products.models import Product
import uuid
import datetime


class Order(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=30, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    # Delivery info (stored at time of order)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    payment_method = models.CharField(max_length=50, default='COD')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Razorpay fields for secure Live tracking
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mrp_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.ForeignKey('cart.Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Timestamps — created_at is set ONCE on creation, never regenerated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            year = datetime.datetime.now().year
            short_id = str(uuid.uuid4().int)[:4]
            self.order_id = f'GRO-{year}-{short_id}'
        
        # Auto-update COD payment status based on delivery status
        if self.payment_method == 'COD':
            if self.status == 'delivered':
                self.payment_status = 'paid'
            else:
                self.payment_status = 'pending'
            
        super().save(*args, **kwargs)

    def get_item_total(self):
        """Sum of all order item subtotals."""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_status_display_label(self):
        status_map = {
            'confirmed': 'Confirmed',
            'processing': 'Processing',
            'out_for_delivery': 'Out for Delivery',
            'delivered': 'Delivered',
            'cancelled': 'Cancelled',
            # Legacy support
            'pending': 'Pending',
            'shipped': 'Out for Delivery',
        }
        return status_map.get(self.status, self.status.title())

    def get_tracking_step(self):
        """Returns 1-4 integer for which step is active."""
        step_map = {
            'confirmed': 1,
            'processing': 2,
            'out_for_delivery': 3,
            'delivered': 4,
            # Legacy
            'pending': 1,
            'shipped': 3,
        }
        return step_map.get(self.status, 1)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.price * self.quantity


class SupportTicket(models.Model):
    ISSUE_CHOICES = [
        ('late_delivery', 'Late Delivery'),
        ('wrong_item', 'Wrong Item Received'),
        ('payment_issue', 'Payment Issue'),
        ('damaged_item', 'Damaged Item'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_tickets')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_tickets')
    ticket_id = models.CharField(max_length=30, unique=True, blank=True)
    issue_type = models.CharField(max_length=30, choices=ISSUE_CHOICES, default='other')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            year = datetime.datetime.now().year
            short_id = str(uuid.uuid4().int)[:4]
            self.ticket_id = f'TICK-{year}-{short_id}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.ticket_id} – {self.get_issue_type_display()} ({self.user.username})"

    class Meta:
        ordering = ['-created_at']