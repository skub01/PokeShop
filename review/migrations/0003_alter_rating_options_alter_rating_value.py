# Generated by Django 5.0 on 2023-12-24 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_alter_rating_options_remove_rating_name_rating_value'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={},
        ),
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.IntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')]),
        ),
    ]