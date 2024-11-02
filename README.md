# BirdShop657 #

A small Wagtail web shop app with Stripe integration.

## Compatible ##

### Tested with ###

``` Python
django==5.x.x
wagtail==6.1.1
wagtailmedia==0.15.1
```

## Installation ###

### Pip requirements ###

``` Python
pip install -r requirements.txt
```

## Development ##

### Stripe CLI ###

    stripe login

    stripe listen --forward-to localhost/webhooks/stripe/

### Build a new release ###

``` bash
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install black
    python3 -m black . -S -t py310 -t py311 -t py312 --diff
    python3 -m black . -S -t py310 -t py311 -t py312
```

Update version in setup.cfg

Update CHANGELOG.md

``` bash
   python3 -m pip install build
   python3 -m build
```

```Git
   git commit -a -m 'Cangelog message.'
   git push
```

### Todo: ###

 - 0.5.0a
    * Customers request products by email page
    * Improved documentation
 - 0.6.0a
    * product_page_title field on PaymentHistory
    * Create and set listed fields static in a PaymentHistoryAdmin
        * product_page
        * product_page_title
        * sku
        * external_product_id
        * external_price_id
        * price
 - 0.7.0b
    * ProductFiles model
 - 0.8.0b
    * protectedProductFile field on ProductPage
 - 0.9.0b
    * Improved Success page design
    * Improved Cancel page design
 - 0.10.0
    * Tests
 - 1.0.0
    * Release Tag 1.0.0
 - 1.1.0a
    * GDPR pop up?
 - 1.2.0a
    * Embedded form
