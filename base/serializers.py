from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style = {'input_type':'password'},  
    )
    class Meta:
        model = User
        fields = ('email','name','tc','password','password2')
        extra_kwargs = {
            'password':{'write_only':True}
                }
    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password2')
        if password1 != password2:
            raise serializers.ValidationError("Passwords must match")
        return attrs

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user