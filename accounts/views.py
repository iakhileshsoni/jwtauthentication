from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken


# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistration(APIView): 
    renderer_classes = [UserRenderer] # to display 'errors' in top of the any kind of error 
    def post(self, request, format=None): 
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user) # it will generate token for user and that we can pass in response
        return Response({'token': token, 'message': 'Registration Successful'}, status=status.HTTP_201_CREATED)

 
class UserLogin(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email') 
        password = serializer.data.get('password') 
        user = authenticate(email=email, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'Login Successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
            


class UserProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password Changed Successfully'}, status=status.HTTP_200_OK)



class SendPasswordResetEmail(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = SendPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password Reset link sent to registered email. Please check your email to reset your password'}, status=status.HTTP_200_OK)

    

class UserPasswordReset(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password Reset Successfully'}, status=status.HTTP_200_OK)


