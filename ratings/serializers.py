from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Rating
        fields = ['id', 'value', 'user', 'auction']
        read_only_fields = ['id', 'user']