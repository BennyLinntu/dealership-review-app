"""
Serializers for dealership_project
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from djangoapp.models import Dealer, Review, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'phone', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'dealer', 'user', 'rating', 'review_text', 'sentiment',
                  'sentiment_score', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at',
                            'updated_at', 'sentiment', 'sentiment_score']


class DealerSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Dealer
        fields = ['id', 'business_name', 'full_name', 'email', 'phone', 'address',
                  'city', 'state', 'zip_code', 'latitude', 'longitude', 'image_url',
                  'created_at', 'updated_at', 'reviews']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DealerDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Dealer
        fields = ['id', 'business_name', 'full_name', 'email', 'phone', 'address',
                  'city', 'state', 'zip_code', 'latitude', 'longitude', 'image_url',
                  'created_at', 'updated_at', 'reviews']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        UserProfile.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


class SentimentAnalysisSerializer(serializers.Serializer):
    text = serializers.CharField()
