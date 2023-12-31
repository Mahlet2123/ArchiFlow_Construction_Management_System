# Generated by Django 4.2.5 on 2023-11-05 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_events'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectScheduleEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.project')),
            ],
            options={
                'db_table': 'tblevents',
            },
        ),
        migrations.DeleteModel(
            name='Events',
        ),
    ]
