"""
Views for dealership_project
"""
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import TemplateView
from rest_framework import generics, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from djangoapp.forms import RegisterForm
from djangoapp.models import Dealer, Review, UserProfile
from djangoapp.sentiment import analyze_sentiment
from djangoapp.serializers import (
    DealerDetailSerializer,
    DealerSerializer,
    LoginSerializer,
    RegisterSerializer,
    ReviewSerializer,
    SentimentAnalysisSerializer,
)

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
STATE_NAMES = dict(Dealer.STATE_CHOICES)


def resolve_state(value):
    """Accept either a full state name or a two-letter abbreviation."""
    if not value:
        return ''
    value = value.strip()
    return STATE_MAP.get(value.lower(), value.upper())


def safe_next(request, fallback='/'):
    candidate = request.POST.get('next') or request.GET.get('next')
    if candidate and url_has_allowed_host_and_scheme(
        candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return fallback


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


# Frontend Views


class IndexView(View):
    def get(self, request):
        dealers = Dealer.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            num_reviews=Count('reviews', distinct=True),
        ).order_by('business_name')

        state_filter = request.GET.get('state', '').strip()
        query = request.GET.get('q', '').strip()

        if state_filter:
            dealers = dealers.filter(state=resolve_state(state_filter))
        if query:
            dealers = dealers.filter(
                Q(business_name__icontains=query)
                | Q(full_name__icontains=query)
                | Q(city__icontains=query)
                | Q(state__icontains=query)
            )

        active_states = (
            Dealer.objects.values_list('state', flat=True)
            .distinct()
            .order_by('state')
        )
        state_options = [
            {'code': code, 'name': STATE_NAMES.get(code, code)}
            for code in active_states
        ]

        return render(request, 'index.html', {
            'dealers': dealers,
            'state_filter': state_filter,
            'state_options': state_options,
            'search_query': query,
            'total_dealers': dealers.count(),
        })


class AboutView(TemplateView):
    template_name = 'About.html'


class ContactView(TemplateView):
    template_name = 'Contact.html'


class LoginPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login_page.html', {'next': request.GET.get('next', '')})

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(safe_next(request))
        return render(
            request,
            'login_page.html',
            {
                'error': 'Invalid username or password.',
                'next': request.POST.get('next', ''),
                'username': username,
            },
            status=401,
        )


class RegisterPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register_page.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
            )
            login(request, user)
            messages.success(request, 'Welcome! Your account is ready.')
            return redirect(safe_next(request, '/'))
        return render(request, 'register_page.html', {'form': form}, status=400)


class LogoutPageView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class DealerDetailPageView(View):
    def get(self, request, dealer_id):
        dealer = get_object_or_404(
            Dealer.objects.annotate(
                avg_rating=Avg('reviews__rating'),
                num_reviews=Count('reviews', distinct=True),
            ),
            id=dealer_id,
        )
        reviews = Review.objects.filter(dealer=dealer).select_related('user')
        return render(request, 'dealer_detail.html', {
            'dealer': dealer,
            'reviews': reviews,
            'average_rating': dealer.avg_rating or 0,
            'review_count': dealer.num_reviews,
        })


class PostReviewPageView(View):
    def _context(self, dealer, **extra):
        from vehicles.models import CarMake, CarModel
        context = {
            'dealer': dealer,
            'car_makes': CarMake.objects.order_by('name'),
            'car_models': CarModel.objects.order_by('make__name', 'name'),
            'today': date.today().isoformat(),
            'current_year': date.today().year,
        }
        context.update(extra)
        return context

    def get(self, request, dealer_id):
        dealer = get_object_or_404(Dealer, id=dealer_id)
        if not request.user.is_authenticated:
            return redirect(f'/login/?next=/dealer/{dealer_id}/add_review/')
        return render(request, 'post_review.html', self._context(dealer))

    def post(self, request, dealer_id):
        dealer = get_object_or_404(Dealer, id=dealer_id)
        if not request.user.is_authenticated:
            return redirect(f'/login/?next=/dealer/{dealer_id}/add_review/')

        review_text = request.POST.get('review', '').strip()
        rating_raw = request.POST.get('rating', '')
        car_year_raw = request.POST.get('car_year', '').strip()
        purchase_date = parse_date(request.POST.get('purchase_date'))
        car_year = int(car_year_raw) if car_year_raw.isdigit() else None
        errors = []

        if len(review_text) < 10:
            errors.append('Please write at least 10 characters.')
        if len(review_text) > 2000:
            errors.append('Reviews cannot be longer than 2000 characters.')
        if rating_raw not in {'1', '2', '3', '4', '5'}:
            errors.append('Choose a rating between 1 and 5.')
        if car_year is not None and not 1900 <= car_year <= 2100:
            errors.append('Enter a valid car year.')

        if errors:
            return render(
                request,
                'post_review.html',
                self._context(
                    dealer,
                    errors=errors,
                    review_text=review_text,
                    rating=rating_raw,
                    car_year=car_year_raw,
                    purchase_date=request.POST.get('purchase_date', ''),
                    selected_make=request.POST.get('car_make', ''),
                    selected_model=request.POST.get('car_model', ''),
                ),
                status=400,
            )

        analysis = analyze_sentiment(review_text)
        Review.objects.create(
            dealer=dealer,
            user=request.user,
            rating=int(rating_raw),
            review_text=review_text,
            sentiment=analysis['sentiment'],
            sentiment_score=analysis['polarity_score'],
            car_make=request.POST.get('car_make', '').strip()[:100],
            car_model=request.POST.get('car_model', '').strip()[:100],
            car_year=car_year,
            purchase=bool(request.POST.get('purchase')),
            purchase_date=purchase_date,
        )
        messages.success(request, 'Your review was posted. Thanks for sharing!')
        return redirect('dealer-detail-page', dealer_id=dealer.id)

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
        except Token.DoesNotExist:
            return Response({
                'message': 'Already logged out'
            }, status=status.HTTP_200_OK)


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
    serializer_class = DealerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Dealer.objects.annotate(
                avg_rating=Avg('reviews__rating'),
                num_reviews=Count('reviews', distinct=True),
            )
            .prefetch_related('reviews__user')
            .order_by('business_name')
        )


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
    queryset = Review.objects.select_related('user', 'dealer').all()
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
        return Review.objects.filter(dealer_id=dealer_id).select_related('user')

# Sentiment Analysis View


class SentimentAnalysisView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SentimentAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            analysis = analyze_sentiment(text)
            return Response({
                'text': text,
                'sentiment': analysis['sentiment'],
                'polarity_score': analysis['polarity_score'],
                'subjectivity_score': analysis['subjectivity_score'],
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
        username = request.data.get(
            'userName', request.data.get('username', ''))
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'userName': user.username,
                'status': 'Authenticated',
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
                'short_name': d.business_name,
                'business_name': d.business_name,
                'address': d.address,
                'city': d.city,
                'state': d.state,
                'zip': d.zip_code,
                'lat': d.latitude,
                'long': d.longitude,
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
            'short_name': d.business_name,
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

    def get(self, request, state):
        state_abbr = resolve_state(state)
        dealers = Dealer.objects.filter(state=state_abbr).order_by('id')
        dealers_list = []
        for d in dealers:
            dealers_list.append({
                'id': d.id,
                'full_name': d.full_name,
                'short_name': d.business_name,
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
        reviews = Review.objects.filter(dealer_id=dealer_id).select_related('user')
        reviews_list = []
        for r in reviews:
            reviews_list.append({
                'id': r.id,
                'name': r.user.username if r.user else 'Anonymous',
                'dealership': dealer_id,
                'review': r.review_text,
                'purchase': r.purchase,
                'purchase_date': (
                    str(r.purchase_date) if r.purchase_date
                    else str(r.created_at.date())
                ),
                'car_make': r.car_make,
                'car_model': r.car_model,
                'car_year': r.car_year,
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
            })
        return Response({'CarModels': car_models}, status=status.HTTP_200_OK)


class AnalyzeSentimentView(views.APIView):
    """Analyze sentiment via GET - /analyze/<text>"""
    permission_classes = [AllowAny]

    def get(self, request, text):
        analysis = analyze_sentiment(text)
        return Response({
            'sentiment': analysis['sentiment'],
            'polarity_score': analysis['polarity_score'],
        }, status=status.HTTP_200_OK)
