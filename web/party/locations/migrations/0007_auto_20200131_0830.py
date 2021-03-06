from django.db import migrations


DISTRICTS = [
    {'name': 'Баткенская область', 'slug': 'batkenskaya-oblast', 'id': 2},
    {'name': 'Чуйская область', 'slug': 'chuyskaya-oblast', 'id': 3},
    {'name': 'Джалал-Абадская область', 'slug': 'dzhalal-abadskaya-oblast', 'id': 4},
    {'name': 'Нарынская область', 'slug': 'narynskaya-oblast', 'id': 5},
    {'name': 'Ошская область', 'slug': 'oshskaya-oblast', 'id': 6},
    {'name': 'Таласская область', 'slug': 'talasskaya-oblast', 'id': 7},
    {'name': 'Иссык-Кульская область', 'slug': 'issyk-kulskaya-oblast', 'id': 8},
]

REGIONS = [
    {'name': 'Первомайский район', 'slug': 'pervomayskiy-rayon', 'id': 1},
    {'name': 'Свердловский район', 'slug': 'sverdlovskiy-rayon', 'id': 2},
    {'name': 'Октябрьский район', 'slug': 'oktyabrskiy-rayon', 'id': 3},
    {'name': 'Ленинский район', 'slug': 'leninskiy-rayon', 'id': 4},]


DISTRICTS_AND_REGIONS = {'Чуйская область':['Первомайский район','Свердловский район','Октябрьский район','Ленинский район'],
                         'Таласская область':['Бакай-Атинский район','Кара-Бууринский район','Манасский район',
                                              'Таласский район','Ак-Суйский район'],
                         'Иссык-Кульская область':['Джети-Огузский район','Тонский район','Тюпский район','Иссык-Кульский район'],
                         'Нарынская область':['Ак-Талинский район','Ат-Башинский район','Жумгальский район',
                                              'Кочкорский район','Нарынский район'],
                         'Джалал-Абадская область':[],
                         'Ошская область':['Алайский район','Араванский район','Кара-Кулджинский район','Кара-Суйский район',
                                           'Ноокатский район','Узгенский район','Чон-Алайский район'],
                         'Баткенская область':['Баткенский район','Кадамжайский район','Лейлекский район']
}

class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_region_district'),
    ]

    def migrate_district_region_relation(apps, schema_editor):
        Region = apps.get_model('locations', 'Region')
        District = apps.get_model('locations', 'District')

        District.objects.all().delete()

        for district in DISTRICTS:
            District.objects.get_or_create(district_id=district['id'], slug=district['slug'], name=district['name'])

        Region.objects.filter(region_id__in=[2, 3, 4, 5, 6, 7, 8]).delete()

        for region in REGIONS:
            Region.objects.get_or_create(slug=region['slug'], name=region['name'], defaults={'region_id': region['id']})

        for dist, regions in DISTRICTS_AND_REGIONS.items():
            district_obj = District.objects.get(name=dist)
            for r in regions:
                region_obj = Region.objects.get(name=r)
                region_obj.district = district_obj
                region_obj.save()


    def revert(apps, scema):
        pass

    operations = [
        migrations.RunPython(migrate_district_region_relation, revert),
    ]
