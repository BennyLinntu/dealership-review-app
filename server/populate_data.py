"""
Script to populate the database with sample dealers and cars
"""
from djangoapp.models import Dealer
from vehicles.models import CarMake, CarModel
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership_project.settings')
django.setup()


# Sample dealers - 50 dealers across US states
dealers_data = [
    {'business_name': 'Downtown Toyota', 'full_name': 'John Thompson', 'email': 'john@downtowntoyota.com',
        'phone': '(555) 123-4567', 'address': '123 Main Street', 'city': 'New York', 'state': 'NY', 'zip_code': '10001', 'latitude': 40.7128, 'longitude': -74.0060, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Kansas City Honda', 'full_name': 'Sarah Davis', 'email': 'sarah@kchonda.com',
        'phone': '(555) 234-5678', 'address': '456 Oak Avenue', 'city': 'Kansas City', 'state': 'KS', 'zip_code': '66101', 'latitude': 39.0997, 'longitude': -94.5786, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Sunshine Ford', 'full_name': 'Michael Johnson', 'email': 'michael@sunshineford.com',
        'phone': '(555) 345-6789', 'address': '789 Beach Road', 'city': 'Miami', 'state': 'FL', 'zip_code': '33101', 'latitude': 25.7617, 'longitude': -80.1918, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'West Coast BMW', 'full_name': 'Emily Smith', 'email': 'emily@westcoastbmw.com',
        'phone': '(555) 456-7890', 'address': '321 Pacific Highway', 'city': 'Los Angeles', 'state': 'CA', 'zip_code': '90001', 'latitude': 34.0522, 'longitude': -118.2437, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Texas Motors', 'full_name': 'Robert Wilson', 'email': 'robert@texasmotors.com',
        'phone': '(555) 567-8901', 'address': '555 Lone Star Lane', 'city': 'Houston', 'state': 'TX', 'zip_code': '77001', 'latitude': 29.7604, 'longitude': -95.3698, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Chicago Auto Group', 'full_name': 'Amanda Lee', 'email': 'amanda@chicagoauto.com',
        'phone': '(555) 678-9012', 'address': '101 Michigan Avenue', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60601', 'latitude': 41.8781, 'longitude': -87.6298, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Seattle Subaru', 'full_name': 'David Park', 'email': 'david@seattlesubaru.com',
        'phone': '(555) 789-0123', 'address': '200 Pike Street', 'city': 'Seattle', 'state': 'WA', 'zip_code': '98101', 'latitude': 47.6062, 'longitude': -122.3321, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Phoenix Nissan', 'full_name': 'Lisa Martinez', 'email': 'lisa@phoenixnissan.com',
        'phone': '(555) 890-1234', 'address': '300 Desert Road', 'city': 'Phoenix', 'state': 'AZ', 'zip_code': '85001', 'latitude': 33.4484, 'longitude': -112.0740, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Denver Audi', 'full_name': 'Chris Brown', 'email': 'chris@denevaudi.com',
        'phone': '(555) 901-2345', 'address': '400 Mile High Drive', 'city': 'Denver', 'state': 'CO', 'zip_code': '80201', 'latitude': 39.7392, 'longitude': -104.9903, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Atlanta Mercedes', 'full_name': 'Jessica Williams', 'email': 'jessica@atlantamercedes.com',
        'phone': '(555) 012-3456', 'address': '500 Peachtree Street', 'city': 'Atlanta', 'state': 'GA', 'zip_code': '30301', 'latitude': 33.7490, 'longitude': -84.3880, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Boston Volvo', 'full_name': 'Tom Anderson', 'email': 'tom@bostonvolvo.com',
        'phone': '(555) 111-2222', 'address': '600 Newbury Street', 'city': 'Boston', 'state': 'MA', 'zip_code': '02101', 'latitude': 42.3601, 'longitude': -71.0589, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Nashville Hyundai', 'full_name': 'Karen White', 'email': 'karen@nashvillehyundai.com',
        'phone': '(555) 222-3333', 'address': '700 Music Row', 'city': 'Nashville', 'state': 'TN', 'zip_code': '37201', 'latitude': 36.1627, 'longitude': -86.7816, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Portland Kia', 'full_name': 'Brian Taylor', 'email': 'brian@portlandkia.com',
        'phone': '(555) 333-4444', 'address': '800 Broadway', 'city': 'Portland', 'state': 'OR', 'zip_code': '97201', 'latitude': 45.5051, 'longitude': -122.6750, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Las Vegas Lexus', 'full_name': 'Nancy Hall', 'email': 'nancy@lasvegaslexus.com',
        'phone': '(555) 444-5555', 'address': '900 Las Vegas Blvd', 'city': 'Las Vegas', 'state': 'NV', 'zip_code': '89101', 'latitude': 36.1699, 'longitude': -115.1398, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Minneapolis Ford', 'full_name': 'Steven Clark', 'email': 'steven@minneapolisford.com',
        'phone': '(555) 555-6666', 'address': '1000 Lake Street', 'city': 'Minneapolis', 'state': 'MN', 'zip_code': '55401', 'latitude': 44.9778, 'longitude': -93.2650, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'New Orleans Cadillac', 'full_name': 'Patricia Lewis', 'email': 'patricia@nocadillac.com',
        'phone': '(555) 666-7777', 'address': '1100 Bourbon Street', 'city': 'New Orleans', 'state': 'LA', 'zip_code': '70112', 'latitude': 29.9511, 'longitude': -90.0715, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Charlotte Chevrolet', 'full_name': 'Donald Robinson', 'email': 'donald@charlottechevy.com',
        'phone': '(555) 777-8888', 'address': '1200 Trade Street', 'city': 'Charlotte', 'state': 'NC', 'zip_code': '28201', 'latitude': 35.2271, 'longitude': -80.8431, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'San Diego Jeep', 'full_name': 'Sandra Walker', 'email': 'sandra@sandiegodeep.com',
        'phone': '(555) 888-9999', 'address': '1300 Harbor Drive', 'city': 'San Diego', 'state': 'CA', 'zip_code': '92101', 'latitude': 32.7157, 'longitude': -117.1611, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Columbus Honda', 'full_name': 'Mark Young', 'email': 'mark@columbushonda.com',
        'phone': '(555) 999-0000', 'address': '1400 High Street', 'city': 'Columbus', 'state': 'OH', 'zip_code': '43201', 'latitude': 39.9612, 'longitude': -82.9988, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Indianapolis Ram', 'full_name': 'Linda Allen', 'email': 'linda@indyram.com',
        'phone': '(555) 100-2000', 'address': '1500 Monument Circle', 'city': 'Indianapolis', 'state': 'IN', 'zip_code': '46201', 'latitude': 39.7684, 'longitude': -86.1581, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'San Antonio Dodge', 'full_name': 'Charles Scott', 'email': 'charles@sadodge.com',
        'phone': '(555) 200-3000', 'address': '1600 River Walk', 'city': 'San Antonio', 'state': 'TX', 'zip_code': '78201', 'latitude': 29.4241, 'longitude': -98.4936, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Sacramento Toyota', 'full_name': 'Helen Hernandez', 'email': 'helen@sacramentotoyota.com',
        'phone': '(555) 300-4000', 'address': '1700 Capitol Mall', 'city': 'Sacramento', 'state': 'CA', 'zip_code': '95801', 'latitude': 38.5816, 'longitude': -121.4944, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Oklahoma City Ford', 'full_name': 'George Lopez', 'email': 'george@okcford.com',
        'phone': '(555) 400-5000', 'address': '1800 Broadway', 'city': 'Oklahoma City', 'state': 'OK', 'zip_code': '73101', 'latitude': 35.4676, 'longitude': -97.5164, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Omaha Volkswagen', 'full_name': 'Betty King', 'email': 'betty@omahavw.com',
        'phone': '(555) 500-6000', 'address': '1900 Dodge Street', 'city': 'Omaha', 'state': 'NE', 'zip_code': '68101', 'latitude': 41.2565, 'longitude': -95.9345, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Albuquerque Subaru', 'full_name': 'Edward Wright', 'email': 'edward@abqsubaru.com',
        'phone': '(555) 600-7000', 'address': '2000 Central Avenue', 'city': 'Albuquerque', 'state': 'NM', 'zip_code': '87101', 'latitude': 35.0844, 'longitude': -106.6504, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Louisville Chrysler', 'full_name': 'Donna Baker', 'email': 'donna@louisvillechrysler.com',
        'phone': '(555) 700-8000', 'address': '2100 Broadway', 'city': 'Louisville', 'state': 'KY', 'zip_code': '40201', 'latitude': 38.2527, 'longitude': -85.7585, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Tucson Mazda', 'full_name': 'Richard Nelson', 'email': 'richard@tucsonmazda.com',
        'phone': '(555) 800-9000', 'address': '2200 Speedway Blvd', 'city': 'Tucson', 'state': 'AZ', 'zip_code': '85701', 'latitude': 32.2226, 'longitude': -110.9747, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Fresno Buick', 'full_name': 'Barbara Carter', 'email': 'barbara@fresnobuick.com',
        'phone': '(555) 900-0100', 'address': '2300 Blackstone Avenue', 'city': 'Fresno', 'state': 'CA', 'zip_code': '93701', 'latitude': 36.7378, 'longitude': -119.7871, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Sacramento Honda', 'full_name': 'Joseph Mitchell', 'email': 'joseph@sacramentohonda.com',
        'phone': '(555) 010-0200', 'address': '2400 Arden Way', 'city': 'Sacramento', 'state': 'CA', 'zip_code': '95825', 'latitude': 38.6019, 'longitude': -121.4195, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Long Beach Nissan', 'full_name': 'Carol Perez', 'email': 'carol@lbnissan.com',
        'phone': '(555) 020-0300', 'address': '2500 Atlantic Avenue', 'city': 'Long Beach', 'state': 'CA', 'zip_code': '90801', 'latitude': 33.7701, 'longitude': -118.1937, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Mesa Mitsubishi', 'full_name': 'Kenneth Roberts', 'email': 'kenneth@mesamitsubishi.com',
        'phone': '(555) 030-0400', 'address': '2600 Main Street', 'city': 'Mesa', 'state': 'AZ', 'zip_code': '85201', 'latitude': 33.4152, 'longitude': -111.8315, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Aurora Toyota', 'full_name': 'Deborah Turner', 'email': 'deborah@auroratoyota.com',
        'phone': '(555) 040-0500', 'address': '2700 Colfax Avenue', 'city': 'Aurora', 'state': 'CO', 'zip_code': '80010', 'latitude': 39.7294, 'longitude': -104.8319, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Virginia Beach Ford', 'full_name': 'Joshua Phillips', 'email': 'joshua@vbford.com',
        'phone': '(555) 050-0600', 'address': '2800 Atlantic Avenue', 'city': 'Virginia Beach', 'state': 'VA', 'zip_code': '23451', 'latitude': 36.8529, 'longitude': -75.9780, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Raleigh BMW', 'full_name': 'Susan Campbell', 'email': 'susan@raleighbmw.com',
        'phone': '(555) 060-0700', 'address': '2900 Hillsborough Street', 'city': 'Raleigh', 'state': 'NC', 'zip_code': '27601', 'latitude': 35.7796, 'longitude': -78.6382, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Colorado Springs Jeep', 'full_name': 'Timothy Evans', 'email': 'timothy@csjeep.com',
        'phone': '(555) 070-0800', 'address': '3000 Nevada Avenue', 'city': 'Colorado Springs', 'state': 'CO', 'zip_code': '80901', 'latitude': 38.8339, 'longitude': -104.8214, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Bakersfield GMC', 'full_name': 'Shirley Edwards', 'email': 'shirley@bakersfieldgmc.com',
        'phone': '(555) 080-0900', 'address': '3100 Chester Avenue', 'city': 'Bakersfield', 'state': 'CA', 'zip_code': '93301', 'latitude': 35.3733, 'longitude': -119.0187, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Tampa Hyundai', 'full_name': 'Gregory Collins', 'email': 'gregory@tampahyundai.com',
        'phone': '(555) 090-1000', 'address': '3200 Bay Shore Blvd', 'city': 'Tampa', 'state': 'FL', 'zip_code': '33601', 'latitude': 27.9506, 'longitude': -82.4572, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Honolulu Lexus', 'full_name': 'Frances Stewart', 'email': 'frances@honolululexus.com',
        'phone': '(555) 110-1100', 'address': '3300 Kalakaua Avenue', 'city': 'Honolulu', 'state': 'HI', 'zip_code': '96815', 'latitude': 21.3069, 'longitude': -157.8583, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Anchorage Subaru', 'full_name': 'Wayne Morris', 'email': 'wayne@anchoragesubaru.com',
        'phone': '(555) 120-1200', 'address': '3400 Northern Lights Blvd', 'city': 'Anchorage', 'state': 'AK', 'zip_code': '99501', 'latitude': 61.2181, 'longitude': -149.9003, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Baton Rouge Toyota', 'full_name': 'Martha Rogers', 'email': 'martha@batonrougetoyota.com',
        'phone': '(555) 130-1300', 'address': '3500 Florida Blvd', 'city': 'Baton Rouge', 'state': 'LA', 'zip_code': '70801', 'latitude': 30.4515, 'longitude': -91.1871, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Des Moines Ford', 'full_name': 'Raymond Reed', 'email': 'raymond@desmoinesford.com',
        'phone': '(555) 140-1400', 'address': '3600 Grand Avenue', 'city': 'Des Moines', 'state': 'IA', 'zip_code': '50301', 'latitude': 41.5868, 'longitude': -93.6250, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Wichita Chevrolet', 'full_name': 'Angela Cook', 'email': 'angela@wichitachevy.com',
        'phone': '(555) 150-1500', 'address': '3700 Douglas Avenue', 'city': 'Wichita', 'state': 'KS', 'zip_code': '67201', 'latitude': 37.6872, 'longitude': -97.3301, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Providence Honda', 'full_name': 'Joe Bailey', 'email': 'joe@providencehonda.com',
        'phone': '(555) 160-1600', 'address': '3800 Westminster Street', 'city': 'Providence', 'state': 'RI', 'zip_code': '02901', 'latitude': 41.8240, 'longitude': -71.4128, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Richmond Dodge', 'full_name': 'Lori Bell', 'email': 'lori@richmonddodge.com',
        'phone': '(555) 170-1700', 'address': '3900 Broad Street', 'city': 'Richmond', 'state': 'VA', 'zip_code': '23218', 'latitude': 37.5407, 'longitude': -77.4360, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Salt Lake City Nissan', 'full_name': 'Albert Richardson', 'email': 'albert@slcnissan.com',
        'phone': '(555) 180-1800', 'address': '4000 State Street', 'city': 'Salt Lake City', 'state': 'UT', 'zip_code': '84101', 'latitude': 40.7608, 'longitude': -111.8910, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Jackson Mazda', 'full_name': 'Sara Cox', 'email': 'sara@jacksonmazda.com',
        'phone': '(555) 190-1900', 'address': '4100 State Street', 'city': 'Jackson', 'state': 'MS', 'zip_code': '39201', 'latitude': 32.2988, 'longitude': -90.1848, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Cheyenne Buick', 'full_name': 'Eric Howard', 'email': 'eric@cheyennebuick.com',
        'phone': '(555) 200-2000', 'address': '4200 Central Avenue', 'city': 'Cheyenne', 'state': 'WY', 'zip_code': '82001', 'latitude': 41.1400, 'longitude': -104.8202, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Burlington Audi', 'full_name': 'Christine Ward', 'email': 'christine@burlingtonauto.com',
        'phone': '(555) 210-2100', 'address': '4300 Main Street', 'city': 'Burlington', 'state': 'VT', 'zip_code': '05401', 'latitude': 44.4759, 'longitude': -73.2121, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Little Rock Mercedes', 'full_name': 'Samuel Torres', 'email': 'samuel@lrmercedes.com',
        'phone': '(555) 220-2200', 'address': '4400 Main Street', 'city': 'Little Rock', 'state': 'AR', 'zip_code': '72201', 'latitude': 34.7465, 'longitude': -92.2896, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Billings Toyota', 'full_name': 'Janet Peterson', 'email': 'janet@billingstoyota.com',
        'phone': '(555) 230-2300', 'address': '4500 Grand Avenue', 'city': 'Billings', 'state': 'MT', 'zip_code': '59101', 'latitude': 45.7833, 'longitude': -108.5007, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Fargo Ford', 'full_name': 'Ryan Gray', 'email': 'ryan@fargoford.com',
        'phone': '(555) 240-2400', 'address': '4600 Broadway', 'city': 'Fargo', 'state': 'ND', 'zip_code': '58101', 'latitude': 46.8772, 'longitude': -96.7898, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
    {'business_name': 'Sioux Falls Chevrolet', 'full_name': 'Victoria Ramirez', 'email': 'victoria@siouxfallschevy.com',
        'phone': '(555) 250-2500', 'address': '4700 Minnesota Avenue', 'city': 'Sioux Falls', 'state': 'SD', 'zip_code': '57101', 'latitude': 43.5446, 'longitude': -96.7311, 'image_url': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400'},
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
