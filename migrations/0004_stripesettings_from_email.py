# Generated by Django 5.0.7 on 2024-07-27 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birdshop657', '0003_paymenthistory_sent_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripesettings',
            name='FROM_EMAIL',
            field=models.CharField(blank=True, help_text='Your from email', max_length=255, null=True),
        ),
    ]
