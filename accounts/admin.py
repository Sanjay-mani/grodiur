from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Address, UserPreference

# Unregister default User admin
admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Info'
    fields = ('phone',)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        "display_name",
        "phone_number",
        "display_email",
        "login_method",
        "is_staff",
    )
    
    # Custom Fieldsets
    fieldsets = (
        (None, {"fields": ("password",)}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


    def display_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        if full_name:
            return full_name
        return "Profile Incomplete"
    display_name.short_description = "FULL NAME"

    def phone_number(self, obj):
        # Prefer numeric username, fallback to profile phone
        if obj.username.isdigit():
            return obj.username
        profile_phone = getattr(obj.profile, 'phone', '')
        return profile_phone if profile_phone else "-"
    phone_number.short_description = "PHONE"

    def display_email(self, obj):
        if obj.email and "@phone.grodiur.com" in obj.email:
            return "Not Provided"
        return obj.email or "Not Provided"
    display_email.short_description = "EMAIL"

    def login_method(self, obj):
        if obj.username.isdigit():
            return "Phone OTP"
        if not obj.email:
            return "Phone OTP"
        return "Email Login"
    login_method.short_description = "LOGIN TYPE"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'city', 'address_type', 'is_default')
    list_filter = ('address_type', 'is_default', 'city')

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_updates', 'offers', 'delivery_alerts')
