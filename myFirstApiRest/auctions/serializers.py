from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema_field
from .models import Category, Auction, Bid

class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

    

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AuctionListCreateSerializer(serializers.ModelSerializer):

    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        closing_date = data.get("closing_date")
        rating = data.get("rating")

        if closing_date and closing_date < timezone.now() + timedelta(days=15):
            raise serializers.ValidationError({
                "closing_date": "Closing date must be at least 15 days after creation date."
            })
        
        if not (1 <= rating <= 5):
            raise serializers.ValidationError({
                "rating": "Rating must be between 1 and 5"
            })

        return data

    class Meta:
        model = Auction
        fields = '__all__'


    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()


class AuctionDetailSerializer(serializers.ModelSerializer):

    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        closing_date = data.get("closing_date")
        rating = data.get("rating")

        if closing_date and closing_date < timezone.now() + timedelta(days=15):
            raise serializers.ValidationError({
                "closing_date": "Closing date must be at least 15 days after creation date."
            })
        
        if not (1 <= rating <= 5):
            raise serializers.ValidationError({
                "rating": "Rating must be between 1 and 5"
            })

        return data

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

class BidSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    def validate(self, data):
        auction = data['auction']
        price = data['price']
        isOpen = data['isOpen']

        # 1. Verificar si la subasta está abierta
        if not isOpen:
            raise serializers.ValidationError("La subasta ya ha cerrado. No se puede pujar.")

        # 2. Verificar si la puja es mayor que la actual
        highest_bid = auction.bids.order_by('-price').first()
        if highest_bid and price <= highest_bid.price:
            raise serializers.ValidationError("La puja debe ser mayor que la anterior puja ganadora.")

        return data
    
    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ('auction',) 