# Generated by Django 2.2 on 2020-05-29 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0014_auto_20200529_0924'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('name',), 'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
    ]
