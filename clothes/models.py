from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

class Sale(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=50, blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='sales_pics')
    created = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        ordering = ['-date_posted', '-created']


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sales-detail', kwargs={'pk':self.pk})

class LikePost(models.Model):
    post_id = models.CharField(max_length=1000)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class SalesRecord(models.Model):
    clients = models.IntegerField()
    projects = models.IntegerField()
    hours_of_support = models.IntegerField()
    workers = models.IntegerField()

    def get_absolute_url(self):
        return reverse('salesRecord-detail', kwargs={'pk':self.pk})

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    Bio = models.TextField()
    test_image = models.ImageField(upload_to='sales_pics')
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('testimony-detail', kwargs={'pk':self.pk})


    class Meta:
        ordering = ['-date_posted']
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated']
    def __str__(self):
        return self.body
