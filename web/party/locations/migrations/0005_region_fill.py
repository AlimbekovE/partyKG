# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-07 04:20
from __future__ import unicode_literals

from django.db import migrations


_data = [
    {'name': 'Джети-Огузский район', 'slug': 'dzheti-oguzskii-raion', 'id': 10},
    {'name': 'Тонский район', 'slug': 'tonskii-raion', 'id': 11},
    {'name': 'Тюпский район', 'slug': 'tiupskii-raion', 'id': 12},
    {'name': 'Иссык-Кульский район', 'slug': 'issyk-kulskii-raion', 'id': 13},
    {'name': 'Ак-Талинский район', 'slug': 'ak-talinskii-raion', 'id': 14},
    {'name': 'Ат-Башинский район', 'slug': 'at-bashinskii-raion', 'id': 15},
    {'name': 'Жумгальский район', 'slug': 'zhumgalskii-raion', 'id': 16},
    {'name': 'Кочкорский район', 'slug': 'kochkorskii-raion', 'id': 17},
    {'name': 'Нарынский район', 'slug': 'narynskii-raion', 'id': 18},
    {'name': 'Алайский район', 'slug': 'alaiskii-raion', 'id': 19},
    {'name': 'Араванский район', 'slug': 'aravanskii-raion', 'id': 20},
    {'name': 'Кара-Кулджинский район', 'slug': 'kara-kuldzhinskii-raion', 'id': 21},
    {'name': 'Кара-Суйский район', 'slug': 'kara-suiskii-raion', 'id': 22},
    {'name': 'Ноокатский район', 'slug': 'nookatskii-raion', 'id': 23},
    {'name': 'Узгенский район', 'slug': 'uzgenskii-raion', 'id': 24},
    {'name': 'Чон-Алайский район', 'slug': 'chon-alaiskii-raion', 'id': 25},
    {'name': 'Баткенский район', 'slug': 'batkenskii-raion', 'id': 26},
    {'name': 'Кадамжайский район', 'slug': 'kadamzhaiskii-raion', 'id': 27},
    {'name': 'Лейлекский район', 'slug': 'leilekskii-raion', 'id': 28},

    {'name': 'Бакай-Атинский район', 'slug': 'bakai-atinskii-raion', 'id': 29},
    {'name': 'Кара-Бууринский район', 'slug': 'kara-buurinskii-raion', 'id': 30},
    {'name': 'Манасский район', 'slug': 'manasskii-raion', 'id': 31},
    {'name': 'Таласский район', 'slug': 'talasskii-raion', 'id': 32},
    {'name': 'Ак-Суйский район', 'slug': 'ak-suiskii-raion', 'id': 33},
]


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_fill_city_model'),
    ]

    def qwerty(apps, schema_editor):
        Region = apps.get_model('locations', 'Region')

        for x in _data:
            Region.objects.get_or_create(region_id=x['id'], slug=x['slug'], name=x['name'])



    def revert(apps, scema):
        pass

    operations = [
        migrations.RunPython(qwerty, revert),
    ]
