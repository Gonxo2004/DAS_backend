from django.db import models
from django.core.validators import MinValueValidator
from users.models import CustomUser
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

class Auction(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField(validators=[MinValueValidator(1)])
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE)
    stock = models.IntegerField(validators=[MinValueValidator(1)])
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='auctions', on_delete=models.CASCADE)
    thumbnail = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.title

    def get_average_rating(self):
        average = self.ratings.aggregate(Avg('value'))['value__avg']
        return round(average, 2) if average else 1  # Redondear a 2 decimales o devolver None si no hay valoraciones

class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name="bids", on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    creation_date = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(CustomUser, related_name="bids", on_delete=models.CASCADE)

    class Meta:
        ordering = ('id', 'price')

    def __str__(self):
        return f"Bid {self.id} for {str(self.auction)}"
