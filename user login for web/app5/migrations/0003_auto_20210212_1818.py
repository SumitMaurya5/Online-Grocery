# Generated by Django 2.2.12 on 2021-02-12 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app5', '0002_auto_20210212_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
