# Generated by Django 4.2.3 on 2023-10-02 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_remove_blog_comments_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_header_image',
            field=models.ImageField(default='blog_headers/default_header.jpg', upload_to='blog_headers/'),
        ),
    ]
