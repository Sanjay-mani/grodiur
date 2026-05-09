from django.db import models
from django.conf import settings
from products.models import Product


class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐ 1 - Very Bad'),
        (2, '⭐⭐ 2 - Bad'),
        (3, '⭐⭐⭐ 3 - Average'),
        (4, '⭐⭐⭐⭐ 4 - Good'),
        (5, '⭐⭐⭐⭐⭐ 5 - Excellent'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    order = models.ForeignKey(
        'orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}⭐"

    def get_stars(self):
        return '⭐' * self.rating