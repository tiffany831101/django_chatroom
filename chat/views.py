from rest_framework.response import Response
from .models import Earthquake, Location, EarthquakeRecord
from .serializers import (
    EarthquakeSerializer,
    LocationSerializer,
    EarthquakeRecondSerializer,
)
from rest_framework import viewsets


class EarthquakeViewSet(viewsets.ModelViewSet):
    queryset = Earthquake.objects.all()
    serializer_class = EarthquakeSerializer


class EarthquakeRecordViewSet(viewsets.ModelViewSet):
    queryset = EarthquakeRecord.objects.all()
    serializer_class = EarthquakeRecondSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
