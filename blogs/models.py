from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    BLOG_TYPE_CHOICES = (
        ('basic', 'Basic Blog'),
        ('premium', 'Premium Blog'),
    )
    BLOG_TOPIC_CHOICES = (
        ('none', 'Select Topic'),
        ('Finance', 'Finance'),
        ('Business', 'Business'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Design and Development', 'Design and Development'),
        ('Technology', 'Technology'),
        ('Education', 'Education'),
        ('News', 'News'),
        ('Entertainment', 'Entertainment'),
        ('Travel', 'Travel'),
        ('Food and Drink', 'Food and Drink'),
        ('Beauty and Fashion', 'Beauty and Fashion'),
        ('Health and Fitness', 'Health and Fitness'),
        ('Relationships', 'Relationships'),
        ('Gaming', 'Gaming'),
        ('Science and Medicine', 'Science and Medicine'),
        ('Home Ownership', 'Home Ownership'),
        ('Lifestyle and Hobbies', 'Lifestyle and Hobbies'),
        ('Pets', 'Pets'),
        ('Your Own Journey', 'Your Own Journey')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=150)
    blog_type = models.CharField(max_length=10, choices=BLOG_TYPE_CHOICES, default='basic')
    blog_topic = models.CharField(choices=BLOG_TOPIC_CHOICES, default='none')
    blog_summary = models.CharField(max_length=200)
    blog_content = models.CharField(max_length=5000)
    is_published = models.BooleanField(default=False)
    blog_date_time = models.DateTimeField(auto_now=True)
    blog_likes_count = models.IntegerField(default=0)
    blog_header_image = models.ImageField(upload_to='blog_headers/', default='blog_headers/hero_1.jpg')

    def __str__(self):
        return self.blog_title + ' by ' + self.user.username

