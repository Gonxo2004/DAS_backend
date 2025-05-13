from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from auctions.models import Auction
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsOwnerOrReadOnly

class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(auction_id=self.kwargs['auction_id'])\
                              .order_by('-creation_date')

    def perform_create(self, serializer):
        auction = get_object_or_404(Auction, id=self.kwargs['auction_id'])
        serializer.save(user=self.request.user, auction=auction)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(auction_id=self.kwargs['auction_id'])