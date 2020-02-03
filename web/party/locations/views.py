from rest_framework import generics
from rest_framework.response import Response

from party.locations.models import City, District, Region
from party.locations.serializers import CitySerializer, DistrictSerializer, RegionSerializer


class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class RegionList(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DistrictList(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
