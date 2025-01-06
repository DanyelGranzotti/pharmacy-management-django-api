from rest_framework import serializers
from ..models.user import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ..models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'cost_price', 'profit_margin', 'quantity']
        ref_name = 'UserProductSerializer'

class UserSerializer(serializers.ModelSerializer):
    purchased_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'status', 'created_at', 'updated_at', 'purchased_products']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'password2')
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs['user'] = user
        return attrs

class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
