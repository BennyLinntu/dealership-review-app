from django.contrib import admin
from vehicles.models import CarMake, CarModel


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'year')
    search_fields = ('name', 'make__name')
    list_filter = ('make', 'year')
