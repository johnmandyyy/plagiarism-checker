# Generated by Django 4.2.2 on 2024-05-25 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_credibility_is_plagirized'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('day', models.IntegerField()),
                ('month', models.IntegerField()),
            ],
        ),
    ]