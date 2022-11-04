from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=64)
    image = models.CharField(max_length=500)

    def __str__(self):
        return self.categoryName


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    status = models.BooleanField(default=True)
    img_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name="category_items")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_items")
    
    def __str__(self):
        return self.title



class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner} bidding on {self.listing}"


class Comment(models.Model):
    message = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.message


class Watchlist(models.Model):
    listing = models.ManyToManyField(Listing, blank=True, related_name="original")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s watchlist"