from django.contrib import admin

# Register your models here.
from .models import PaymentHistory

# make static
""" product_page, product_page_tilte, sku, external_product_id, external_price_id, price
"""


admin.site.register(PaymentHistory)
