# Generated by Django 5.0 on 2023-12-14 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_alter_category_options_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='series',
            field=models.CharField(default='XY', max_length=255),
        ),
    ]
