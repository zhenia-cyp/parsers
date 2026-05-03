from django.db import models

from django.db import models


class BrainProduct(models.Model):
    title = models.TextField(
        null=True,
        blank=True
    )

    manufacturer = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    color = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    memory = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    price_regular = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    price_sale = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    images = models.JSONField(
        default=list,
        blank=True
    )

    product_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True
    )
    reviews_count = models.IntegerField(
        null=True,
        blank=True
    )
    screen_diagonal = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    screen_resolution = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    characteristics = models.JSONField(
        default=dict,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Brain Product"
        verbose_name_plural = "Brain Products"
