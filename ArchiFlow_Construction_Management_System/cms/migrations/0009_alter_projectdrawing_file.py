# Generated by Django 4.2.5 on 2023-11-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_alter_projectdocument_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdrawing',
            name='file',
            field=models.FileField(upload_to='drawing_uploads/'),
        ),
    ]