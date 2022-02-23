from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    #required field
    title = models.CharField(max_length=64)
    price = models.FloatField()

    #optional data
    desc = models.CharField(max_length=500, blank=True)
    url = models.CharField(max_length=128, blank=True)
    followers = models.ManyToManyField(User, related_name="watchlist", blank=True)
    category = models.ManyToManyField(Category, related_name="listings", blank=True)

    #auto data
    created_at = models.DateTimeField(auto_now_add=True)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} is ${self.price}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bidding = models.FloatField()

    def __str__(self):
        return f"{self.user} bid ${self.bidding} on {self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments_made")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.commenter}: "{self.comment}"'

