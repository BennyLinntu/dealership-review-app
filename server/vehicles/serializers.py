"""
Serializers for vehicles app
"""
from rest_framework import serializers
from vehicles.models import CarMake, CarModel


class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['id', 'name', 'description']


class CarModelSerializer(serializers.ModelSerializer):
    make = CarMakeSerializer(read_only=True)

    class Meta:
        model = CarModel
        fields = ['id', 'make', 'name', 'year']


class CarMakeDetailSerializer(serializers.ModelSerializer):
    models = CarModelSerializer(many=True, read_only=True)

    class Meta:
        model = CarMake
        fields = ['id', 'name', 'description', 'models']
