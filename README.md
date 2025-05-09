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

   Set your webhook signing secret in wagtail admin.

### Stripe Dashboard ###

   Get API keys from the [dashboard](https://dashboard.stripe.com/test/apikeys).

### Build and publish a new release ###

#### Black ####

``` bash
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install black
    python3 -m black . -S -t py310 -t py311 -t py312 --diff
    python3 -m black . -S -t py310 -t py311 -t py312
```

#### Update version ###

Use [Trunk Based Development](https://trunkbaseddevelopment.com/), [Semver](semver.org) and [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

Update version in VERSION.txt

Update CHANGELOG.md

#### Build ####

``` bash
   python3 -m pip install build
   python3 -m build
```

#### Commit and Push ####

```Git
   git commit -a -m 'Cangelog message.'
   git push
```

### Todo: ###

 - 0.6.0a
    * Customers request products by email page
    * Improved documentation
 - 0.7.0a
    * [Migrating from ModelAdmin to Wagtail’s built-in features](https://wagtail-modeladmin.readthedocs.io/en/latest/migrating.html#migrating-from-modeladmin-to-wagtail-s-built-in-features)
 - 0.8.0b
    * ProductFiles model
 - 0.9.0b
    * protectedProductFile field on ProductPage
 - 0.10.0b
    * Improved Success page design
    * Improved Cancel page design
 - 0.11.0
    * Tests
 - 1.0.0
    * Release Tag 1.0.0
 - 1.1.0a
    * GDPR pop up?
 - 1.2.0a
    * Embedded form
