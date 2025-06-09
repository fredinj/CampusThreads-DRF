from django.urls import path
from rest_framework import routers
from accounts.views import LoginAPIView, RegisterAPIView, LogoutAPIView, CheckAuthAPIView, VerifyVerificationAPIView, SendVerificationAPIView

router = routers.DefaultRouter()


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login-endpoint"),
    path('signup/', RegisterAPIView.as_view(), name="register-endpoint"),
    path('logout/', LogoutAPIView.as_view(), name="logout-endpoint"),
    path('check-auth/', CheckAuthAPIView.as_view(), name="check-auth-endpoint"),
    path('send-verify-email/', SendVerificationAPIView.as_view(), name='send-verification-email'),
    path('verify-email/', VerifyVerificationAPIView.as_view(), name='verify-email-endpoint')
]

urlpatterns += router.urls