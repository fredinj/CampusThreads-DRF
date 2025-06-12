from django.urls import path
from rest_framework import routers

from accounts.views import LoginAPIView, RegisterAPIView, LogoutAPIView, CheckAuthAPIView
from accounts.views import VerifyVerificationAPIView, SendVerificationAPIView, UserProfileAPIView

router = routers.DefaultRouter()

urlpatterns = [
    #Authentication endpoints
    path('auth/login/', LoginAPIView.as_view(), name="login-endpoint"),
    path('auth/signup/', RegisterAPIView.as_view(), name="register-endpoint"),
    path('auth/logout/', LogoutAPIView.as_view(), name="logout-endpoint"),
    path('auth/check-auth/', CheckAuthAPIView.as_view(), name="check-auth-endpoint"),
    path('auth/send-verify-email/', SendVerificationAPIView.as_view(), name='send-verification-email'),
    path('auth/verify-email/', VerifyVerificationAPIView.as_view(), name='verify-email-endpoint'),

    # User profile endpoints
    path('user/update/', UserProfileAPIView.as_view(), name='user-profile-update')
]

urlpatterns += router.urls