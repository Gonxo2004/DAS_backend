from django.shortcuts import render
# Create your views here.
from django.db.models import Q
from rest_framework import generics, status
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from .permissions import IsOwnerOrAdmin, IsBidderOrAdmin

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all() #consulta a base de datos (que dato devuelvo)
    serializer_class = CategoryListCreateSerializer #llamada al serializador (como lo devuelvo)
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class AuctionListCreate(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOwnerOrAdmin()]
        return [AllowAny()]

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
    permission_classes = [IsOwnerOrAdmin]
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    

class BidListCreate(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    serializer_class = BidSerializer
    def get_queryset(self): # obtengo todas las pujas de la subatasa concreta
        return Bid.objects.filter(auction_id=self.kwargs['auction_id'])  

    def perform_create(self, serializer):
        auction = Auction.objects.get(pk=self.kwargs['auction_id'])  
        serializer.save(auction=auction)  

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsBidderOrAdmin]
    queryset = Bid.objects.all()
    serializer_class = BidSerializer


class UserAuctionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
    # Obtener las subastas del usuario autenticado
        user_auctions = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(user_auctions, many=True)
        return Response(serializer.data)

    