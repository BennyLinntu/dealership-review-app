"""
Serializers for dealership_project
"""
from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import serializers

from djangoapp.models import Dealer, Review, UserProfile
from djangoapp.sentiment import analyze_sentiment


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
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'dealer', 'user', 'reviewer_name', 'rating', 'review_text',
            'sentiment', 'sentiment_score', 'car_make', 'car_model',
            'car_year', 'purchase', 'purchase_date', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'reviewer_name', 'created_at', 'updated_at', 'sentiment',
            'sentiment_score',
        ]

    def get_reviewer_name(self, obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return "Anonymous"

    def validate_review_text(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Please write at least 10 characters.")
        if len(value) > 2000:
            raise serializers.ValidationError(
                "Reviews cannot be longer than 2000 characters.")
        return value

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_car_year(self, value):
        if value is not None and not 1900 <= value <= 2100:
            raise serializers.ValidationError("Enter a valid car year.")
        return value

    def create(self, validated_data):
        analysis = analyze_sentiment(validated_data.get('review_text', ''))
        validated_data['sentiment'] = analysis['sentiment']
        validated_data['sentiment_score'] = analysis['polarity_score']
        return super().create(validated_data)


class DealerSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    state_name = serializers.CharField(source='get_state_display', read_only=True)

    class Meta:
        model = Dealer
        fields = [
            'id', 'business_name', 'full_name', 'email', 'phone', 'address',
            'city', 'state', 'state_name', 'zip_code', 'latitude', 'longitude',
            'image_url', 'average_rating', 'review_count', 'created_at',
            'updated_at', 'reviews',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        value = getattr(obj, 'avg_rating', None)
        if value is None:
            value = obj.reviews.aggregate(value=Avg('rating'))['value']
        return round(float(value or 0), 2)

    def get_review_count(self, obj):
        value = getattr(obj, 'num_reviews', None)
        if value is None:
            value = obj.reviews.count()
        return int(value or 0)


class DealerDetailSerializer(DealerSerializer):
    class Meta(DealerSerializer.Meta):
        fields = DealerSerializer.Meta.fields


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists.")
        return value.lower()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        UserProfile.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


class SentimentAnalysisSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=5000)
