# Generated by Django 2.2 on 2020-05-30 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0015_auto_20200529_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.District', verbose_name='Область'),
        ),
    ]
