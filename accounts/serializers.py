from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User

from accounts.models import CustomerUser, BrndAdmin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class CustomerUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomerUser
        fields = ['phone_number', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer_user = CustomerUser.objects.create(user=user, **validated_data)
        return customer_user


class BrndAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BrndAdmin
        fields = ['phone_number', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        brand_admin = BrndAdmin.objects.create(user=user, **validated_data)
        return brand_admin


class LogInSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token
