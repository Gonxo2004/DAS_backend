from django.shortcuts import render
from django.contrib.auth.password_validation import validate_password

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    # Asegúrate de agregar LogoutSerializer en serializers.py (lo incluyo aquí abajo)
)

# -------------------------------------------------------------------
#  Serializer mínimo para Logout (puedes moverlo a serializers.py)
# -------------------------------------------------------------------
from rest_framework import serializers

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh token a revocar")


# -------------------------------------------------------------------
#  CRUD de usuarios
# -------------------------------------------------------------------
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": serializer.data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.request.method in ["PATCH", "PUT"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]


# -------------------------------------------------------------------
#  Perfil del usuario autenticado
# -------------------------------------------------------------------
class UserProfileView(RetrieveUpdateDestroyAPIView):
    """
    GET    → Ver mi perfil  
    PATCH  → Actualizar parcialmente mi perfil  
    DELETE → Borrar mi cuenta
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# -------------------------------------------------------------------
#  Logout (revocar refresh token)
# -------------------------------------------------------------------
class LogoutView(APIView):
    """
    Realiza el logout revocando el refresh token suministrado.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer  # ← añadido

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


# -------------------------------------------------------------------
#  Cambio de contraseña
# -------------------------------------------------------------------
class ChangePasswordView(APIView):
    """
    Cambia la contraseña del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer  # ← añadido

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        user = request.user
        if not user.check_password(old_password):
            return Response(
                {"old_password": "Incorrect current password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response(
                {"new_password": e.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )
