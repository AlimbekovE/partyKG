from django.contrib import admin
from party.locations.models import Region, District, City


class RegionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Region, RegionAdmin)

class DistrictAdmin(admin.ModelAdmin):
    pass
admin.site.register(District, DistrictAdmin)

class CityAdmin(admin.ModelAdmin):
    pass
admin.site.register(City, CityAdmin)
