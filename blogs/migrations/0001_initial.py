# Generated by Django 4.2 on 2023-08-23 09:15

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
            name='Blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_title', models.CharField(max_length=150)),
                ('blog_type', models.CharField(choices=[('basic', 'Basic Blog'), ('premium', 'Premium Blog')], default='basic', max_length=10)),
                ('blog_topic', models.CharField(choices=[('none', 'Select Topic'), ('Finance', 'Finance'), ('Business', 'Business'), ('Marketing', 'Marketing'), ('Sales', 'Sales'), ('Design and Development', 'Design and Development'), ('Technology', 'Technology'), ('Education', 'Education'), ('News', 'News'), ('Entertainment', 'Entertainment'), ('Travel', 'Travel'), ('Food and Drink', 'Food and Drink'), ('Beauty and Fashion', 'Beauty and Fashion'), ('Health and Fitness', 'Health and Fitness'), ('Relationships', 'Relationships'), ('Gaming', 'Gaming'), ('Science and Medicine', 'Science and Medicine'), ('Home Ownership', 'Home Ownership'), ('Lifestyle and Hobbies', 'Lifestyle and Hobbies'), ('Pets', 'Pets'), ('Your Own Journey', 'Your Own Journey')], default='none')),
                ('blog_summary', models.CharField(max_length=200)),
                ('blog_content', models.CharField(max_length=5000)),
                ('is_published', models.BooleanField(default=False)),
                ('blog_date_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
