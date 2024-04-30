from rest_framework import serializers
from .models import Earthquake, EarthquakeRecord, Location
import secrets
from django.contrib.auth.hashers import make_password


class EarthquakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earthquake
        fields = "__all__"


class EarthquakeRecondSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarthquakeRecord
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
