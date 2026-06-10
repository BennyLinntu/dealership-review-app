"""
Views for vehicles app
"""
from rest_framework import generics
from rest_framework.permissions import AllowAny
from vehicles.models import CarMake, CarModel
from vehicles.serializers import CarMakeSerializer, CarModelSerializer, CarMakeDetailSerializer


class CarMakeListView(generics.ListAPIView):
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializer
    permission_classes = [AllowAny]


class CarModelListView(generics.ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [AllowAny]


class CarListView(generics.ListAPIView):
    """List all car makes with their models"""
    queryset = CarMake.objects.all()
    serializer_class = CarMakeDetailSerializer
    permission_classes = [AllowAny]
