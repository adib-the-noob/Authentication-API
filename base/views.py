from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,UserLoginSerializer
from django.contrib.auth import authenticate


class UserRegistration(APIView):
    def post(self,request,format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'message':serializer.data},
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )
        
class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user =  authenticate(email=email,password=password)
            if user is not None:
                return Response(
                    {'message':'Login Successful'},
                    status=status.HTTP_200_OK
                    )
            else:
                return Response({'error':{'non_field_errors' : ['Email or Password is not Valid!']}},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'Login'})
