from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=30)

class Listing(models.Model):
    title = models.CharField(max_length=80, blank=False)
    description = models.CharField(max_length=1000, blank=False)
    starting_bid = models.DecimalField(max_digits=20, decimal_places=2, blank=False)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self:id}: {self.title} {self.description} {self.starting_bid}"


class Bid(models.Model):
    pass

class Comment(models.Model):
    pass