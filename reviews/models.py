from django.conf import settings
from django.db import models
from core.models import TimeStampedModel
from catalog.models import Product


class Review(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(
        blank=True,
        null=True
    )
    is_public = models.BooleanField(default=True)

    class Meta:
        unique_together = ("product", "buyer")
        indexes = [models.Index(fields=["product", "created_at"]) ]
