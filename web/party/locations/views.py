from rest_framework import generics
from rest_framework.response import Response

from party.locations.models import City, District, Region
from party.locations.serializers import CitySerializer, DistrictSerializer, RegionSerializer


class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None


class RegionList(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        district = request.query_params.get('district')
        if district:
            queryset = queryset.filter(district=district)
        serializer = RegionSerializer(queryset, many=True,
                                      context={'request': request})
        return Response(serializer.data)


class DistrictList(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    pagination_class = None
