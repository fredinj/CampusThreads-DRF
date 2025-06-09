from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from accounts.models import User
from accounts.serializers import RegisterSerializer


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User Created Successfully!"}, status=status.HTTP_201_CREATED
        )


class LogoutAPIView(APIView):
    # commenting to make it easier to test with postman
    # permission_classes = [permissions.IsAuthenticated]

    # refresh tokens aren't used for now so we're sending a dummy response
    def post(self, request):
        return Response({"message": "Logged out successfully"})


class CheckAuthAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            "authenticated": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "emailVerified": user.email_verified
            },
            "message": "Authenticated"
        })
        
    def handle_exceptions(self, e):
        if isinstance(e, (AuthenticationFailed, NotAuthenticated)):
            return Response(
                {"authenticated": False, "message": "No token provided or authorization denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().handle_exception(e)
    

class SendVerificationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request):
        user = request.user
        
        # Skip if the user is already verified
        if user.email_verified:
            return Response({"message": "User is already verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = user.generate_email_verification_token()
        verification_url = f"{settings.CLIENT_URL}/verify-email?token={token_str}"
        email_body=f"""
        <p>Hi {user.first_name},</p>
        <p>Please click the link below to verify your email address:</p>
        <a href="{verification_url}">Verify Email</a>
        <p>If you did not register for an account, please ignore this email.</p>
        """
        
        msg = EmailMultiAlternatives(
            subject="Verify you email - CampusThreads",
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        
        msg.attach_alternative(email_body, "text/html")
        msg.send(fail_silently=False)
        
        
        # send_mail(
        #     subject="Verify you email - CampusThreads",
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[user.email],
        #     message=email_body,
        #     fail_silently=False,
        # )
        
        return Response({ "message": 'Verification email sent successfully.' }, status=status.HTTP_200_OK)
    
class VerifyVerificationAPIView(APIView):
    # Allow logged out users verify their accounts
    permission_classes = [permissions.AllowAny]
    
    def put(self, request):
        req_token = request.query_params.get('token')
        if not req_token:
            return Response({"message": "Token is not provided"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email_verification_token=req_token)
        verification_status = user.verify_email_token(req_token)
        if verification_status:
            return Response({"message":"Email verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "An error occurred while verifying your email"}, status=status.HTTP_400_BAD_REQUEST)