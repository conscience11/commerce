from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title=models.CharField(max_length=64)
    description=models.TextField()
    owner=models.CharField(max_length=64)
    category=models.CharField(max_length=64, null=True, blank=True)
    url=models.URLField(blank=True, null=True)
    price=models.CharField(max_length=5000000000000000, default='$0')
    date=models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.id}: {self.title} {self.price}"

class Comment(models.Model):
    commenter=models.CharField(max_length=64)
    comment=models.TextField()
    listid=models.IntegerField()
    time=models.DateTimeField()
    def __str__(self):
        return f"{self.commenter} comments {self.comment} on list {self.listid} on {self.time}"

class Wlist(models.Model):
    owner=models.CharField(max_length=64)
    listid=models.IntegerField()
    def __str__(self):
        return f"{self.owner} {self.listid}"



class Bid(models.Model):
    bidder=models.CharField(max_length=64)
    bid=models.CharField(max_length=5000000000000000)
    listid=models.IntegerField()
    def __str__(self):
        return f"{self.id}: {self.bidder} bids ${self.bid} on list {self.listid}"

class ClosedListing(models.Model):
    datecreated=models.DateTimeField()
    dateclosed=models.DateTimeField()
    owner=models.CharField(max_length=64)
    winner=models.CharField(max_length=64, null=True, blank=True)
    winprice=models.CharField(max_length=5000000000000000)
    url=models.URLField()
    category=models.CharField(max_length=500)
    description=models.TextField()
    title=models.CharField(max_length=80, null=True, blank=True)
    listid=models.CharField(max_length=500000000000000, null=True, blank=True)
    def __str__(self):
        return f"{self.owner} {self.winprice} {self.title} {self.winner}"

