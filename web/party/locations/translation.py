from modeltranslation.translator import translator, TranslationOptions
from party.locations.models import City, District, Region


class CityTranslationOptions(TranslationOptions):
    fields = ('name',)


class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)


class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(City, CityTranslationOptions)
translator.register(District, DistrictTranslationOptions)
translator.register(Region, RegionTranslationOptions)
