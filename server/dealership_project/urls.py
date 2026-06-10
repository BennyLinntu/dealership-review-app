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

    # Frontend Pages
    path('', djangoapp_views.IndexView.as_view(), name='index'),
    path('about/', djangoapp_views.AboutView.as_view(), name='about'),
    path('contact/', djangoapp_views.ContactView.as_view(), name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
