from rest_framework import serializers
from party.locations.models import City, District, Region


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ('name',)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ('name',)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        exclude = ('name',)
