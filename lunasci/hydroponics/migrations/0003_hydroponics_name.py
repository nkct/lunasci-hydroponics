# Generated by Django 5.1.6 on 2025-02-18 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hydroponics', '0002_sensorreading'),
    ]

    operations = [
        migrations.AddField(
            model_name='hydroponics',
            name='name',
            field=models.CharField(default='Hydroponics', max_length=512),
        ),
    ]
