# Generated by Django 3.2.9 on 2021-11-22 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FIT', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='attended',
            field=models.BooleanField(default=False),
        ),
    ]
