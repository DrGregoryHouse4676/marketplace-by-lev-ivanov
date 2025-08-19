from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "buyer",
        "rating",
        "is_public",
        "created_at"
    )
    list_filter = ("is_public", "rating")
