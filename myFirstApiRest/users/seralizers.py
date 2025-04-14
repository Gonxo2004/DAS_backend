from rest_framework import serializers
from .models import CustomUser
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'birth_date', 'municipality',
                  'locality', 'password')
        extra_kwargs = {'password': {'write_only': True},}

    def validate_email(self, value):
        user = self.instance  # Solo tiene valor cuando se está actualizando
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
    def validate_username(self, value):
        user = self.instance  # Solo tiene valor cuando se está actualizando
        if CustomUser.objects.filter(username=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError("Username already in use.")
        return value

    def validate(self, data):
        # Validación de edad
        birth_date = data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                raise serializers.ValidationError("You must be at least 18 years old.")
        return data

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)