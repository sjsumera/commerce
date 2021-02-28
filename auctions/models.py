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
    current_bid = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=30, blank=True)
    active = models.BooleanField(default=True)
    selling_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="seller")
    bidding_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="buyer")

    def __str__(self):
        return f"{self.id}: {self.title} {self.description} {self.starting_bid} {self.active}"


class Bid(models.Model):
    bid = models.DecimalField(max_digits=20, decimal_places=2, blank=False)
    bidding_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.bidding_user} bid ${self.bid} on {self.listing.title}"

class Comment(models.Model):
    comment = models.CharField(max_length=1000, blank=False)
    post_date = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.comment} {self.post_date}"