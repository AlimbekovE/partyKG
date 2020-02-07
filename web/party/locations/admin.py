from django.contrib import admin
from party.locations.models import Region, District, City


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'region_id', 'district')
    list_filter = ('district',)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'district_id')


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city_id')


admin.site.register(City, CityAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
