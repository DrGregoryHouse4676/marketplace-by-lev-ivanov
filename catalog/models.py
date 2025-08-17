from django.db import models
from django.utils.text import slugify
from core.models import TimeStampedModel, CurrencyChoices
from accounts.models import SellerProfile


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("parent", "slug")
        indexes = [models.Index(fields=[
            "parent",
            "slug"])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    seller = models.ForeignKey(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name="products"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=220,
        unique=True
    )
    description = models.TextField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.UAH
    )
    quantity = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=False)  # activate after moderation

    class Meta:
        indexes = [
            models.Index(fields=["category", "is_active"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image_url = models.URLField(
        blank=True,
        null=True
    )
    image_file = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "id"]
