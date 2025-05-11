from django.db import models
from django.conf import settings
from auctions.models import Auction, CustomUser
from django.core.exceptions import ValidationError

class Comment(models.Model):
    title       = models.CharField(max_length=50)
    body        = models.TextField()
    creation_date  = models.DateTimeField(auto_now_add=True)
    last_modification_date  = models.DateTimeField(auto_now=True)
    user        = models.ForeignKey(CustomUser,      # o directamente CustomUser si lo prefieres
                                    related_name='comments',
                                    on_delete=models.CASCADE)
    auction     = models.ForeignKey(Auction,
                                    related_name='comments',
                                    on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} on {self.auction.title} by {self.user.username}"

    