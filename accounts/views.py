from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,RegisterSerializer

User = get_user_model()


# --- REGISTER VIEW ---
class RegisterView(generics.CreateAPIView):
    """
    Publicly accessible.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    """
    Returns the authenticated user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
