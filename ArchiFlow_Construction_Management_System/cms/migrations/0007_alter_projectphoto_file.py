# Generated by Django 4.2.5 on 2023-11-05 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectphoto',
            name='file',
            field=models.FileField(upload_to='project_photos/'),
        ),
    ]