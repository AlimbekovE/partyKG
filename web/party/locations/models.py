from django.db import models


class District(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    district_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    region_id = models.IntegerField()
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('region_id', 'district')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    city_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name
