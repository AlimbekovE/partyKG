# Generated by Django 2.2 on 2020-05-29 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0012_auto_20200529_0841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('city_id',), 'verbose_name': 'City', 'verbose_name_plural': 'Cities'},
        ),
    ]
