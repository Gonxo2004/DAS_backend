from django.shortcuts import render
# Create your views here.
from django.db.models import Q
from rest_framework import generics, status
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidSerializer
from rest_framework.exceptions import ValidationError

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all() #consulta a base de datos (que dato devuelvo)
    serializer_class = CategoryListCreateSerializer #llamada al serializador (como lo devuelvo)

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class AuctionListCreate(generics.ListCreateAPIView):
    serializer_class = AuctionListCreateSerializer

    def get_queryset(self):
        queryset = Auction.objects.all()
        params = self.request.query_params

        search = params.get('search')
        category_id = params.get('category_id')
        min_price = params.get('min_price')
        max_price = params.get('max_price')

        # Search filter
        if search:
            if len(search) < 3:
                raise ValidationError(
                    {"search": "Search query must be at least 3 characters long."},
                    code=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Category filter
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Price filters
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(starting_price__gte=min_price)
            except ValueError:
                raise ValidationError({"min_price": "Must be a valid number."})

        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(starting_price__lte=max_price)
            except ValueError:
                raise ValidationError({"max_price": "Must be a valid number."})

        return queryset

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

    