# Generated by Django 4.2.5 on 2024-05-21 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_research_file_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='research',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
    ]
