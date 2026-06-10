"""
Models for vehicles app
"""
from django.db import models


class CarMake(models.Model):
    """Car manufacturer"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Car model"""
    make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=255)
    year = models.IntegerField()

    class Meta:
        unique_together = ('make', 'name', 'year')

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year})"
