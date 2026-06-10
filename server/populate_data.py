"""
Script to populate the database with sample dealers and cars
"""
from vehicles.models import CarMake, CarModel
from djangoapp.models import Dealer
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership_project.settings')
django.setup()


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
print("Creating dealers...")
for dealer_data in dealers_data:
    dealer, created = Dealer.objects.get_or_create(
        business_name=dealer_data['business_name'],
        defaults=dealer_data
    )
    if created:
        print(f"Created dealer: {dealer.business_name}")
    else:
        print(f"Dealer already exists: {dealer.business_name}")

# Create car makes and models
print("\nCreating cars...")
for make_name, models in cars_data.items():
    make, created = CarMake.objects.get_or_create(
        name=make_name,
        defaults={'description': f'{make_name} vehicles'}
    )
    if created:
        print(f"Created car make: {make_name}")

    for model_name in models:
        for year in range(2020, 2025):
            model, created = CarModel.objects.get_or_create(
                make=make,
                name=model_name,
                year=year
            )
            if created:
                print(f"Created car model: {make_name} {model_name} ({year})")

print("\nDatabase population complete!")
