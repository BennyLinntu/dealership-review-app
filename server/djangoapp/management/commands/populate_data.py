"""
Management command to populate the database with sample data
"""
from django.core.management.base import BaseCommand
from djangoapp.models import Dealer, Review
from djangoapp.sentiment import analyze_sentiment
from vehicles.models import CarMake, CarModel


class Command(BaseCommand):
    help = 'Populate database with sample dealers and cars'

    def handle(self, *args, **options):
        # Sample dealers
        dealers_data = [
            {
                'business_name': 'Downtown Toyota',
                'full_name': 'John Thompson',
                'email': 'john@downtowntoyota.com',
                'phone': '(555) 123-4567',
                'address': '123 Main Street',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10001',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'
            },
            {
                'business_name': 'Kansas City Honda',
                'full_name': 'Sarah Davis',
                'email': 'sarah@kcbonda.com',
                'phone': '(555) 234-5678',
                'address': '456 Oak Avenue',
                'city': 'Kansas City',
                'state': 'KS',
                'zip_code': '66101',
                'latitude': 39.0997,
                'longitude': -94.5786,
                'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'
            },
            {
                'business_name': 'Sunshine Ford',
                'full_name': 'Michael Johnson',
                'email': 'michael@sunshineford.com',
                'phone': '(555) 345-6789',
                'address': '789 Beach Road',
                'city': 'Miami',
                'state': 'FL',
                'zip_code': '33101',
                'latitude': 25.7617,
                'longitude': -80.1918,
                'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'
            },
            {
                'business_name': 'West Coast BMW',
                'full_name': 'Emily Smith',
                'email': 'emily@westcoastbmw.com',
                'phone': '(555) 456-7890',
                'address': '321 Pacific Highway',
                'city': 'Los Angeles',
                'state': 'CA',
                'zip_code': '90001',
                'latitude': 34.0522,
                'longitude': -118.2437,
                'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'
            },
            {
                'business_name': 'Texas Motors',
                'full_name': 'Robert Wilson',
                'email': 'robert@texasmotors.com',
                'phone': '(555) 567-8901',
                'address': '555 Lone Star Lane',
                'city': 'Houston',
                'state': 'TX',
                'zip_code': '77001',
                'latitude': 29.7604,
                'longitude': -95.3698,
                'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'
            }
        ]

        # Car makes and models
        cars_data = {
            'Toyota': ['Camry', 'Corolla', 'Prius', 'Highlander', 'RAV4'],
            'Honda': ['Civic', 'Accord', 'CR-V', 'Odyssey', 'Pilot'],
            'Ford': ['F-150', 'Mustang', 'Fusion', 'Edge', 'Explorer'],
            'BMW': ['3 Series', '5 Series', 'X5', 'Z4', 'M440i'],
            'Chevrolet': ['Silverado', 'Camaro', 'Malibu', 'Equinox', 'Tahoe']
        }

        # Create dealers
        self.stdout.write('Creating dealers...')
        for dealer_data in dealers_data:
            dealer, created = Dealer.objects.get_or_create(
                business_name=dealer_data['business_name'],
                defaults=dealer_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created dealer: {dealer.business_name}'))
            else:
                self.stdout.write(
                    f'Dealer already exists: {dealer.business_name}')

        # Create car makes and models
        self.stdout.write('Creating cars...')
        for make_name, models in cars_data.items():
            make, created = CarMake.objects.get_or_create(
                name=make_name,
                defaults={'description': f'{make_name} vehicles'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created car make: {make_name}'))

            for model_name in models:
                for year in range(2020, 2025):
                    model, created = CarModel.objects.get_or_create(
                        make=make,
                        name=model_name,
                        year=year
                    )
                    if created:
                        self.stdout.write(
                            f'Created car model: {make_name} {model_name} ({year})')

        self.stdout.write(self.style.SUCCESS('Database population complete!'))

        # A few anonymous reviews make the UI useful straight after setup.
        reviews_data = [
            {
                'dealer': 'Downtown Toyota',
                'rating': 5,
                'review_text': (
                    'Fantastic experience from start to finish. The team explained '
                    'every option and never pushed extras. I love my new Camry.'
                ),
                'car_make': 'Toyota',
                'car_model': 'Camry',
                'car_year': 2023,
            },
            {
                'dealer': 'Kansas City Honda',
                'rating': 4,
                'review_text': (
                    'Friendly staff and a fair price. The paperwork took a little '
                    'longer than expected, but the car is excellent.'
                ),
                'car_make': 'Honda',
                'car_model': 'Civic',
                'car_year': 2022,
            },
            {
                'dealer': 'West Coast BMW',
                'rating': 5,
                'review_text': (
                    'Smooth, stress-free purchase. They arranged financing quickly '
                    'and the car was spotless at pickup.'
                ),
                'car_make': 'BMW',
                'car_model': '3 Series',
                'car_year': 2024,
            },
        ]

        for entry in reviews_data:
            dealer = Dealer.objects.filter(
                business_name=entry['dealer']).first()
            if not dealer:
                continue
            analysis = analyze_sentiment(entry['review_text'])
            Review.objects.get_or_create(
                dealer=dealer,
                review_text=entry['review_text'],
                defaults={
                    'rating': entry['rating'],
                    'car_make': entry['car_make'],
                    'car_model': entry['car_model'],
                    'car_year': entry['car_year'],
                    'purchase': True,
                    'sentiment': analysis['sentiment'],
                    'sentiment_score': analysis['polarity_score'],
                },
            )

        self.stdout.write(self.style.SUCCESS('Sample reviews are ready.'))
