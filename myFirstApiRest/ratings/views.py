from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Rating
from .serializers import RatingSerializer
from auctions.models import Auction
from django.shortcuts import get_object_or_404

class RatingListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(auction_id=self.kwargs['auction_id'])

    def perform_create(self, serializer):
        auction = get_object_or_404(Auction, id=self.kwargs['auction_id'])
        serializer.save(user=self.request.user, auction=auction)


class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user, auction_id=self.kwargs['auction_id'])
