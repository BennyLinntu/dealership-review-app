"""
Views for dealership_project
"""
from rest_framework import views, viewsets, status, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView
from textblob import TextBlob
import json

from djangoapp.models import Dealer, Review, UserProfile
from djangoapp.serializers import (
    DealerSerializer, ReviewSerializer, RegisterSerializer,
    LoginSerializer, SentimentAnalysisSerializer, DealerDetailSerializer
)

# Frontend Views


class IndexView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'About.html'


class ContactView(TemplateView):
    template_name = 'Contact.html'

# Authentication Views


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'error': 'Logout failed'
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'message': 'Registration successful'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Dealer Views


class DealerListView(generics.ListAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [AllowAny]


class DealerDetailView(generics.RetrieveAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerDetailSerializer
    permission_classes = [AllowAny]


class DealerByStateView(generics.ListAPIView):
    serializer_class = DealerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        state = self.kwargs['state'].upper()
        return Dealer.objects.filter(state=state)

# Review Views


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class ReviewByDealerView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        dealer_id = self.kwargs['dealer_id']
        return Review.objects.filter(dealer_id=dealer_id)

# Sentiment Analysis View


class SentimentAnalysisView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SentimentAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity

            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

            return Response({
                'text': text,
                'sentiment': sentiment,
                'polarity_score': round(polarity, 4),
                'subjectivity_score': round(analysis.sentiment.subjectivity, 4)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
