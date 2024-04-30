from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)


# the earthquake informations
class Earthquake(models.Model):
    location_desc = models.TextField()
    earthquake_number = models.IntegerField(default=0)
    magnitude = models.IntegerField()
    occur_time = models.DateTimeField()
    depth = models.FloatField()


# every locations records
class EarthquakeRecord(models.Model):
    e_id = models.ForeignKey(Earthquake, on_delete=models.CASCADE)
    l_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    intensity = models.IntegerField()
