from django.contrib import admin
from .models import UserProfile, SellerProfile, Address

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "created_at")

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "status", "created_at")
    list_filter = ("status",)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "is_default", "city", "country")
