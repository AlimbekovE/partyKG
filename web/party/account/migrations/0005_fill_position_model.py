# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-07 04:20
from __future__ import unicode_literals

from django.db import migrations


_data = [
    {'name': 'Депутаты ЖК', 'slug': 'deputaty-zhk'},
    {'name': 'Депутаты городского округа', 'slug': 'deputaty-gorodskogo-okruga'},
    {'name': 'Депутаты айыльного округа', 'slug': 'deputaty-aiylnogo-okruga'},
]


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200112_2308'),
    ]

    def qwerty(apps, schema_editor):
        Position = apps.get_model('account', 'Position')

        for x in _data:
            Position.objects.get_or_create(slug=x['slug'], name=x['name'])

    def revert(apps, scema):
        pass

    operations = [
        migrations.RunPython(qwerty, revert),
    ]
