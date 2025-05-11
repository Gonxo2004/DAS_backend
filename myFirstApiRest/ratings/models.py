from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser
from auctions.models import Auction

class Rating(models.Model):
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(CustomUser, related_name='ratings', on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name='ratings', on_delete=models.CASCADE)


    class Meta:
        unique_together = ('user', 'auction')  # Un usuario solo puede valorar una subasta una vez
        ordering = ("id",)

    def __str__(self):
        return f"Rating {self.value} by {self.user.username} for {self.auction.title}"

