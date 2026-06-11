"""Setup database: create users and add a review"""
from djangoapp.models import Dealer, Review
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import django
import os
import sys
sys.path.insert(
    0, r'C:\Users\Benny\System File\Desktop\it\dealership-review-app\server')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dealership_project.settings'
django.setup()


# Create admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Created admin')
else:
    print('Admin exists')

# Create testuser
if not User.objects.filter(username='testuser').exists():
    tu = User.objects.create_user('testuser', 'testuser@example.com', 'testpass123',
                                  first_name='Test', last_name='User')
    Token.objects.get_or_create(user=tu)
    print('Created testuser')
else:
    tu = User.objects.get(username='testuser')
    print('testuser exists')

# Add reviews
dealer = Dealer.objects.order_by('id').first()
if Review.objects.count() < 2:
    Review.objects.get_or_create(
        dealer=dealer, user=tu, rating=5,
        defaults={
            'review_text': 'Fantastic services! The staff were incredibly helpful. I highly recommend this dealership.',
            'sentiment': 'positive',
            'sentiment_score': 0.8,
        }
    )
    # Add second review
    dealer2 = Dealer.objects.order_by('id')[1]
    Review.objects.get_or_create(
        dealer=dealer2, user=tu, rating=4,
        defaults={
            'review_text': 'Great experience overall. The car selection was excellent.',
            'sentiment': 'positive',
            'sentiment_score': 0.65,
        }
    )
    print('Added reviews')

print(f'Done: {Dealer.objects.count()} dealers, {Review.objects.count()} reviews')
