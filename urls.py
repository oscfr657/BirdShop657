from django.urls import path

from .views import (
    CreateCheckoutSessionView,
    SuccessView,
    CancelView,
    ProductLandingPageView,
    StripeWebhookView,
)

urlpatterns = [
    path('shop/', ProductLandingPageView.as_view(), name='landing'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path(
        'create-checkout-session/<external_price_id>/',
        CreateCheckoutSessionView.as_view(),
        name='create-checkout-session',
    ),
    path('webhooks/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
