"""
URL Configuration for dealership_project
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth_views
from djangoapp import views as djangoapp_views
from vehicles import views as vehicle_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),

    # Authentication
    path('api/login/', djangoapp_views.LoginView.as_view(), name='login'),
    path('api/logout/', djangoapp_views.LogoutView.as_view(), name='logout'),
    path('api/register/', djangoapp_views.RegisterView.as_view(), name='register'),

    # Dealers API
    path('api/dealers/', djangoapp_views.DealerListView.as_view(), name='dealer-list'),
    path('api/dealers/<int:pk>/',
         djangoapp_views.DealerDetailView.as_view(), name='dealer-detail'),
    path('api/dealers/state/<str:state>/',
         djangoapp_views.DealerByStateView.as_view(), name='dealer-by-state'),

    # Reviews API
    path('api/reviews/', djangoapp_views.ReviewListCreateView.as_view(),
         name='review-list-create'),
    path('api/reviews/<int:dealer_id>/',
         djangoapp_views.ReviewByDealerView.as_view(), name='review-by-dealer'),

    # Cars API
    path('api/cars/', vehicle_views.CarListView.as_view(), name='car-list'),
    path('api/cars/makes/', vehicle_views.CarMakeListView.as_view(),
         name='car-make-list'),
    path('api/cars/models/', vehicle_views.CarModelListView.as_view(),
         name='car-model-list'),

    # Sentiment Analysis
    path('api/sentiment/', djangoapp_views.SentimentAnalysisView.as_view(),
         name='sentiment-analysis'),

    # IBM Coursera-style endpoints
    path('djangoapp/login', djangoapp_views.DjangoLoginView.as_view(),
         name='djangoapp-login'),
    path('djangoapp/logout', djangoapp_views.DjangoLogoutView.as_view(),
         name='djangoapp-logout'),
    path('fetchDealers', djangoapp_views.FetchDealersView.as_view(),
         name='fetch-dealers'),
    path('fetchDealer/<int:dealer_id>', djangoapp_views.FetchDealerByIDView.as_view(),
         name='fetch-dealer'),
    path('fetchDealers/<str:state>', djangoapp_views.FetchDealersByStateView.as_view(),
         name='fetch-dealers-by-state'),
    path('fetchReviews/dealer/<int:dealer_id>',
         djangoapp_views.FetchReviewsByDealerView.as_view(),
         name='fetch-reviews'),
    path('djangoapp/get_cars', djangoapp_views.GetCarsView.as_view(),
         name='get-cars'),
    path('analyze/<str:text>', djangoapp_views.AnalyzeSentimentView.as_view(),
         name='analyze'),

    # Frontend Pages
    path('', djangoapp_views.IndexView.as_view(), name='index'),
    path('about/', djangoapp_views.AboutView.as_view(), name='about'),
    path('contact/', djangoapp_views.ContactView.as_view(), name='contact'),
    path('login/', djangoapp_views.LoginPageView.as_view(), name='login-page'),
    path('logout/', djangoapp_views.LogoutPageView.as_view(), name='logout-page'),
    path('dealer/<int:dealer_id>/',
         djangoapp_views.DealerDetailPageView.as_view(), name='dealer-detail-page'),
    path('dealer/<int:dealer_id>/add_review/',
         djangoapp_views.PostReviewPageView.as_view(), name='post-review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
