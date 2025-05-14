from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'title', 'body',
                  'creation_date', 'last_modification_date',
                  'user', 'auction']
        read_only_fields = ['id', 'creation_date', 'last_modification_date', 'user']