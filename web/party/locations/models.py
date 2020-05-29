from django.db import models
from django.utils.translation import gettext as _


class District(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('slug'))
    district_id = models.IntegerField(unique=True, verbose_name=_('district id'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        ordering = ('district_id',)


class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('slug'))
    region_id = models.IntegerField(verbose_name=_('region id'))
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 null=True, verbose_name=_('district'))

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        ordering = ('name',)
        unique_together = ('region_id', 'district')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    city_id = models.IntegerField(unique=True)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ('name',)

    def __str__(self):
        return self.name
