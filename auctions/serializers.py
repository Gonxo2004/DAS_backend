from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema_field
from .models import Category, Auction, Bid

class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AuctionListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    auctioneer = serializers.ReadOnlyField(source='auctioneer.username')

    def validate(self, data):
        closing_date = data.get("closing_date")

        if closing_date and closing_date < timezone.now() + timedelta(days=15):
            raise serializers.ValidationError({
                "closing_date": "Closing date must be at least 15 days after creation date."
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
    auctioneer = serializers.ReadOnlyField(source='auctioneer.username')
    average_rating = serializers.SerializerMethodField()

    def validate(self, data):
        closing_date = data.get("closing_date")

        if closing_date and closing_date < timezone.now() + timedelta(days=15):
            raise serializers.ValidationError({
                "closing_date": "Closing date must be at least 15 days after creation date."
            })

        return data

    class Meta:
        model = Auction
        fields = [
            'id', 'title', 'description', 'price', 'auctioneer', 'stock',
            'brand', 'category', 'thumbnail', 'creation_date', 'closing_date',"isOpen",
            'average_rating'  
        ]

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def get_average_rating(self, obj):
        return obj.get_average_rating()

class AuctionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'title', 'closing_date', 'thumbnail']

class BidSerializer(serializers.ModelSerializer):
    auction = AuctionShortSerializer(read_only=True) 
    bidder = serializers.ReadOnlyField(source='bidder.username')

    class Meta:
        model = Bid
        fields = [
            'id', 'price', 'creation_date',
            'bidder', 'auction'   
        ]
        read_only_fields = ['id', 'creation_date', 'bidder', 'auction']