# Generated by Django 5.0.2 on 2024-06-22 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_profile_displayname_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
