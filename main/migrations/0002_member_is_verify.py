# Generated by Django 3.2.6 on 2021-08-26 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_verify',
            field=models.BooleanField(default=False),
        ),
    ]
