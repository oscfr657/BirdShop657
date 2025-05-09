from django.contrib import admin

# Register your models here.
from .models import PaymentHistory


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "product_page",
        "sku",
        "payment_status",
        )
    exclude = ["product_page"]
    date_hierarchy = "created_at"
    search_fields = ["email"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "sent_email",
        "sku",
        "external_product_id",
        "external_price_id",
        "price",
        ]


admin.site.register(PaymentHistory, PaymentHistoryAdmin)
