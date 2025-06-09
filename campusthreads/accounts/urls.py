from django.urls import path
from rest_framework import routers
from accounts.views import LoginAPIView, RegisterAPIView

router = routers.DefaultRouter()


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login-endpoint"),
    path('register/', RegisterAPIView.as_view(), name="register-endpoint")
]

urlpatterns += router.urls