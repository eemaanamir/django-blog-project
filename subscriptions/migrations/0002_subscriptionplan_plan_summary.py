# Generated by Django 4.2.3 on 2023-10-05 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='plan_summary',
            field=models.CharField(default='No Summary Available', max_length=200),
        ),
    ]
