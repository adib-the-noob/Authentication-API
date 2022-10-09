from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style = {'input_type':'password'},  
        write_only = True
    )
    class Meta:
        model = User
        fields = ('email','name','tc','password','password2')
        extra_kwargs = {
            'password':{'write_only':True}
                }
    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password2')
        if password1 != password2:
            raise serializers.ValidationError("Passwords must match")
        return attrs

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user




class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ('email','password')



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']


class UserChangePasswordSerializer(serializers.Serializer):
    password  = serializers.CharField(max_length=255,style={
        'input_type':'password'},
        write_only=True
        )

    password2 = serializers.CharField(max_length=255,style={
        'input_type':'password'},
        write_only=True
        )

    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        user = self.context.get('user')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords must match")
        user.set_password(password)
        user.save()
        return attrs

class SendPassowrdResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded uid: ",uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token: ',token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password reset link: ',link)
            return attrs
        else:
            raise serializers.ValidationError("There is no user with this email")