from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from wagtail.models import Site

import stripe

from .models import ProductPage, StripeSettings, PaymentHistory


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        site = Site.find_for_request(request)
        product_page = ProductPage.objects.get(
            external_price_id=self.kwargs['external_price_id']
        )
        stripe.api_key = StripeSettings.for_request(request=request).STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': product_page.external_price_id,
                    'quantity': 1,
                },
            ],
            metadata={"external_product_id": product_page.external_product_id},
            mode='payment',
            success_url=site.root_url + '/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=site.root_url + '/cancel/',
        )
        return redirect(checkout_session.url, permanent=False)


class SuccessView(View):
    def get(self, request):
        try:
            stripe.api_key = StripeSettings.for_request(
                request=request
            ).STRIPE_SECRET_KEY
            session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
            external_product_id = session['metadata']['external_product_id']
            product_page = ProductPage.objects.get(
                external_product_id=external_product_id
            )
            customer_email = session['customer_details']['email']
            customer_name = session['customer_details']['name']
            ph = PaymentHistory.objects.get_or_create(
                email=customer_email,
                product_page=product_page,
                external_product_id=external_product_id,
                sku=product_page.sku,
                external_price_id=product_page.external_price_id,
                price=product_page.price,
            )
            context = {
                'product_page': product_page,
                'customer_email': customer_email,
                'customer_name': customer_name,
            }
            return render(request, 'success.html', context)
        except:
            return redirect(to='cancel', permanent=False)


class CancelView(TemplateView):
    template_name = 'cancel.html'


class ProductLandingPageView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        products = ProductPage.objects.live().public().order_by('-go_live_at')
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({'products': products})
        return context


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    """
    Stripe webhook view to handle events.
    """

    def post(self, request, format=None):
        payload = request.body
        stripewebhook_secret = StripeSettings.for_request(
            request=request
        ).STRIPE_WEBHOOK_SECRET
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, stripewebhook_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session['customer_details']['email']
            external_product_id = session['metadata']['external_product_id']
            product_page = ProductPage.objects.get(
                external_product_id=external_product_id
            )
            ph = PaymentHistory.objects.get_or_create(
                email=customer_email,
                product_page=product_page,
                external_product_id=external_product_id,
                sku=product_page.sku,
                external_price_id=product_page.external_price_id,
                price=product_page.price,
                payment_status='P',
            )
            if session.payment_status == "paid":
                ph.payment_status = 'C'
                site = Site.find_for_request(request)
                from_email = StripeSettings.for_request(request=request).FROM_EMAIL
                sent_email = send_mail(
                    subject=f'Your digital product: { product_page.title }',
                    message=f'Thank you for your purchase. Your digital product: { site.root_url }{ product_page.productFile.url }',
                    from_email=from_email,
                    recipient_list=[customer_email],
                    html_message=f'<p>Thank you for your purchase. Your digital product: <a href="{ site.root_url }{ product_page.productFile.url }"><b>{ product_page.title }</b></a></p>',
                )
                if sent_email >= 1:
                    ph.sent_email = timezone.now()
                    ph.save()
        elif event['type'] == 'checkout.session.async_payment_succeeded':
            session = event['data']['object']
            customer_email = session['customer_details']['email']
            external_product_id = session['metadata']['external_product_id']
            product_page = ProductPage.objects.get(
                external_product_id=external_product_id
            )
            ph = PaymentHistory.objects.get_or_create(
                email=customer_email,
                product_page=product_page,
                external_product_id=external_product_id,
                sku=product_page.sku,
                external_price_id=product_page.external_price_id,
                price=product_page.price,
                payment_status='C',
            )
            site = Site.find_for_request(request)
            from_email = StripeSettings.for_request(request=request).FROM_EMAIL
            sent_email = send_mail(
                subject=f'Your digital product: { product_page.title }',
                message=f'Thank you for your purchase. Your digital product: { site.root_url }{ product_page.productFile.url }',
                from_email=from_email,
                recipient_list=[customer_email],
                html_message=f'<p>Thank you for your purchase. Your digital product: <a href="{ site.root_url }{ product_page.productFile.url }"><b>{ product_page.title }</b></a></p>',
            )
            if sent_email >= 1:
                ph.sent_email = timezone.now()
                ph.save()
        elif event['type'] == 'checkout.session.async_payment_failed':
            session = event['data']['object']
            customer_email = session['customer_details']['email']
            external_product_id = session['metadata']['external_product_id']
            product_page = ProductPage.objects.get(
                external_product_id=external_product_id
            )
            ph = PaymentHistory.objects.get_or_create(
                email=customer_email,
                product_page=product_page,
                external_product_id=external_product_id,
                sku=product_page.sku,
                external_price_id=product_page.external_price_id,
                price=product_page.price,
                payment_status='F',
            )
            site = Site.find_for_request(request)
            from_email = StripeSettings.for_request(request=request).FROM_EMAIL
            sent_email = send_mail(
                subject=f'Your payment failed: { product_page.title }',
                message=f'Your payment for: { product_page.title } failed. Please try again! { site.root_url }{ product_page }',
                from_email=from_email,
                recipient_list=[customer_email],
                html_message=f'<p>Your payment for: { product_page.title } failed.<br><a href="{ site.root_url }">Please try again!</a></p>',
            )
            if sent_email >= 1:
                ph.sent_email = timezone.now()
                ph.save()
        # elif charge.succeeded, payment_intent.succeeded, payment_intent.created, charge.updated
        else:
            print(f'Unhandled event type {event}')
            print(f'Unhandled event type {event.type}')

        return HttpResponse(status=200)
