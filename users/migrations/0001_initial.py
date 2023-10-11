# Generated by Django 4.2 on 2023-08-08 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_bio', models.CharField(max_length=200)),
                ('has_credit_card', models.BooleanField(default=False)),
                ('user_type', models.CharField(choices=[('basic', 'Basic User'), ('premium', 'Premium User')], default='basic', max_length=10)),
                ('user_dp', models.ImageField(default='default_user_dp.png', upload_to='user_dps/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
