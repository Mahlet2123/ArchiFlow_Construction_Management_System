# Generated by Django 4.2.5 on 2023-11-05 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_alter_projectscheduleevent_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='projectscheduleevent',
            table='tblevents',
        ),
    ]
