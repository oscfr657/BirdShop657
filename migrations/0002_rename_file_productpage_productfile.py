# Generated by Django 5.0.7 on 2024-07-15 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birdshop657', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productpage',
            old_name='file',
            new_name='productFile',
        ),
    ]
