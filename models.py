from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel,
)
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting
class StripeSettings(BaseSiteSetting):
    STRIPE_PUBLISHABLE_KEY = models.CharField(
        max_length=255, blank=True, null=True, help_text='Your public Stripe key'
    )
    STRIPE_SECRET_KEY = models.CharField(
        max_length=255, blank=True, null=True, help_text='Your secret Stripe key'
    )
    STRIPE_WEBHOOK_SECRET = models.CharField(
        max_length=255, blank=True, null=True, help_text='Your Stripe webhook secret'
    )


class ProductPage(Page):
    sku = models.CharField(max_length=255, blank=True, null=True)
    external_product_id = models.CharField(max_length=100, blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    file = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True,
        null=True,
    )
    url = models.URLField(blank=True, null=True)
    external_price_id = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(default=0)
    exclude_from_sitemap = models.BooleanField(default=False)

    search_fields = Page.search_fields
    promote_panels = Page.promote_panels
    content_panels = Page.content_panels + [
        FieldPanel('sku'),
        FieldPanel('external_product_id'),
        FieldPanel('image'),
        FieldPanel('file'),
        FieldPanel('url'),
        FieldPanel('external_price_id'),
        FieldPanel('price'),
    ]
    settings_panels = [
        FieldPanel('exclude_from_sitemap'),
    ]

    def get_sitemap_urls(self, request=None):
        if self.exclude_from_sitemap:
            return []
        else:
            return super(ProductPage, self).get_sitemap_urls(request=request)

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class PaymentHistory(models.Model):
    PENDING = 'P'
    COMPLETED = 'C'
    FAILED = 'F'
    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (COMPLETED, 'completed'),
        (FAILED, 'failed'),
    )
    payment_status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.EmailField(max_length=100)

    product_page = models.ForeignKey(
        ProductPage, on_delete=models.SET_NULL, blank=True, null=True
    )
    sku = models.CharField(max_length=255, blank=True, null=True)
    external_product_id = models.CharField(max_length=100, blank=True, null=True)
    external_price_id = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.product_page.title
