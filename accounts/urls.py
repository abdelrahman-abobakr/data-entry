from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Register new user
    path('register/', views.RegisterView.as_view(), name='register'),

    # JWT login (token obtain)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # JWT refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Current user profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
