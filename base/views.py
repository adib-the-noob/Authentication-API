from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate


from .serializers import UserSerializer, UserLoginSerializer
from .renderers import UserRenderer

# Using JWT
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# For User Registration
class UserRegistration(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_token_for_user(user)

            return Response(
                {'token': token, 'message': serializer.data},
                status=status.HTTP_201_CREATED
            )
        print(serializer.errors)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# for user login


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_token_for_user(user)
                return Response(
                    {'token': token, 'message': 'Login Successful'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'error': {'non_field_errors': ['Email or Password is not Valid!']}}, status=status.HTTP_4)
        return Response({'message': 'Login'})
