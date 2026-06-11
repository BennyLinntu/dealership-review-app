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


# ============================================================
# IBM Coursera-style endpoints (matching expected URL patterns)
# ============================================================

class DjangoLoginView(views.APIView):
    """Login endpoint returning userName and status:Authenticated"""
    permission_classes = [AllowAny]

    def post(self, request):
        # Accept either 'userName' or 'username'
        username = request.data.get('userName', request.data.get('username', ''))
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'userName': user.username,
                'userEmail': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'status': 'Authenticated',
                'token': token.key,
            }, status=status.HTTP_200_OK)
        return Response({'userName': username, 'status': 'Failed'},
                        status=status.HTTP_401_UNAUTHORIZED)


class DjangoLogoutView(views.APIView):
    """Logout endpoint - GET request, returns {"userName": ""}"""
    permission_classes = [AllowAny]

    def get(self, request):
        # Invalidate token if user is authenticated
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
            except Exception:
                pass
        return Response({'userName': ''}, status=status.HTTP_200_OK)


class FetchDealersView(views.APIView):
    """Fetch all dealers - IBM Coursera /fetchDealers style"""
    permission_classes = [AllowAny]

    def get(self, request):
        dealers = Dealer.objects.all().order_by('id')
        dealers_list = []
        for d in dealers:
            dealers_list.append({
                'id': d.id,
                'full_name': d.full_name,
                'business_name': d.business_name,
                'address': d.address,
                'city': d.city,
                'state': d.state,
                'zip': d.zip_code,
                'lat': d.latitude,
                'long': d.longitude,
                'short_zip': d.zip_code,
            })
        return Response({'dealers': dealers_list}, status=status.HTTP_200_OK)


class FetchDealerByIDView(views.APIView):
    """Fetch single dealer by ID - /fetchDealer/<dealer_id>"""
    permission_classes = [AllowAny]

    def get(self, request, dealer_id):
        try:
            d = Dealer.objects.get(id=dealer_id)
        except Dealer.DoesNotExist:
            return Response({'error': 'Dealer not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'id': d.id,
            'full_name': d.full_name,
            'business_name': d.business_name,
            'address': d.address,
            'city': d.city,
            'state': d.state,
            'zip': d.zip_code,
            'lat': d.latitude,
            'long': d.longitude,
        }, status=status.HTTP_200_OK)


class FetchDealersByStateView(views.APIView):
    """Fetch dealers by state name or abbreviation - /fetchDealers/<state>"""
    permission_classes = [AllowAny]

    STATE_MAP = {
        'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
        'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT',
        'delaware': 'DE', 'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI',
        'idaho': 'ID', 'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA',
        'kansas': 'KS', 'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME',
        'maryland': 'MD', 'massachusetts': 'MA', 'michigan': 'MI',
        'minnesota': 'MN', 'mississippi': 'MS', 'missouri': 'MO',
        'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',
        'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM',
        'new york': 'NY', 'north carolina': 'NC', 'north dakota': 'ND',
        'ohio': 'OH', 'oklahoma': 'OK', 'oregon': 'OR', 'pennsylvania': 'PA',
        'rhode island': 'RI', 'south carolina': 'SC', 'south dakota': 'SD',
        'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT', 'vermont': 'VT',
        'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV',
        'wisconsin': 'WI', 'wyoming': 'WY',
    }

    def get(self, request, state):
        state_abbr = self.STATE_MAP.get(state.lower(), state.upper())
        dealers = Dealer.objects.filter(state=state_abbr).order_by('id')
        dealers_list = []
        for d in dealers:
            dealers_list.append({
                'id': d.id,
                'full_name': d.full_name,
                'business_name': d.business_name,
                'address': d.address,
                'city': d.city,
                'state': d.state,
                'zip': d.zip_code,
                'lat': d.latitude,
                'long': d.longitude,
            })
        return Response({'dealers': dealers_list}, status=status.HTTP_200_OK)


class FetchReviewsByDealerView(views.APIView):
    """Fetch reviews for a dealer - /fetchReviews/dealer/<dealer_id>"""
    permission_classes = [AllowAny]

    def get(self, request, dealer_id):
        reviews = Review.objects.filter(dealer_id=dealer_id)
        reviews_list = []
        for r in reviews:
            reviews_list.append({
                'id': r.id,
                'name': r.user.username if r.user else 'Anonymous',
                'dealership': dealer_id,
                'review': r.review_text,
                'purchase': True,
                'purchase_date': str(r.created_at.date()),
                'car_make': 'Toyota',
                'car_model': 'Camry',
                'car_year': 2021,
                'rating': r.rating,
                'sentiment': r.sentiment or 'neutral',
            })
        return Response({'reviews': reviews_list}, status=status.HTTP_200_OK)


class GetCarsView(views.APIView):
    """Get all car makes and models - /djangoapp/get_cars returning CarModels key"""
    permission_classes = [AllowAny]

    def get(self, request):
        from vehicles.models import CarMake, CarModel
        car_models = []
        for model in CarModel.objects.select_related('make').all():
            car_models.append({
                'CarMake': model.make.name,
                'CarModel': model.name,
                'Year': model.year,
            })
        return Response({'CarModels': car_models}, status=status.HTTP_200_OK)


class AnalyzeSentimentView(views.APIView):
    """Analyze sentiment via GET - /analyze/<text>"""
    permission_classes = [AllowAny]

    def get(self, request, text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        return Response({'sentiment': sentiment}, status=status.HTTP_200_OK)
