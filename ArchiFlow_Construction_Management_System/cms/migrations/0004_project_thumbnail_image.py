# Generated by Django 4.2.5 on 2023-11-01 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_alter_invitation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='thumbnail_image',
            field=models.ImageField(blank=True, default='OIP.jpg', null=True, upload_to='project_thumbnail_images/'),
        ),
    ]
