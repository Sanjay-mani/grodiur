from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True,
        default='profile_pics/default.png'
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=15, default='')
    pincode = models.CharField(max_length=10, default='')
    house_street = models.TextField(default='')
    city = models.CharField(max_length=100, default='')
    address_type = models.CharField(max_length=20, choices=[('Home', 'Home'), ('Work', 'Work'), ('Other', 'Other')], default='Home')
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            # Set all other addresses for this user to non-default
            Address.objects.filter(user=self.user).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.house_street}, {self.city} - {self.pincode}"

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    order_updates = models.BooleanField(default=True)
    offers = models.BooleanField(default=True)
    delivery_alerts = models.BooleanField(default=True)
    hide_phone_email = models.BooleanField(default=False)
    theme_preference = models.CharField(max_length=20, default='light')

    def __str__(self):
        return f"{self.user.username}'s Preferences"