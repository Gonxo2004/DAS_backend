from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all() #consulta a base de datos (que dato devuelvo)
    serializer_class = CategoryListCreateSerializer #llamada al serializador (como lo devuelvo)

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class AuctionListCreate(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListCreateSerializer

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

class BidListCreate(generics.ListCreateAPIView):
    serializer_class = BidSerializer

    def get_queryset(self): # obtengo todas las pujas de la subatasa concreta
        return Bid.objects.filter(auction_id=self.kwargs['auction_id'])  

    def perform_create(self, serializer):
        auction = Auction.objects.get(pk=self.kwargs['auction_id'])  
        serializer.save(auction=auction)  

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    