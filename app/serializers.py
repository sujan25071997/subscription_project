from rest_framework import serializers

from app import models
from .models import (StripeSubscription,MyStripeModel,CurrentSubscription,)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password':{
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class SubscriptionSerializer(serializers.ModelSerializer):
    """ Serializer for stripe subscription"""

    class Meta:
        model = StripeSubscription
        fields = '__all__'

class MyStripeSerializer(serializers.ModelSerializer):
    """ Serializer for stripe subscription"""

    class Meta:
        model = MyStripeModel
        fields = '__all__'

class CurrentSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentSubscription
        fields = '__all__'
