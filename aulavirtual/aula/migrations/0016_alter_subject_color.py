# Generated by Django 3.2.3 on 2021-06-10 15:48

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aula', '0015_auto_20210608_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='color',
            field=colorfield.fields.ColorField(blank=True, choices=[('#FF923C', 'orange'), ('#2544FF', 'blue'), ('#3AFF51', 'green'), ('#FF1D1D', 'red'), ('#F6FF35', 'yellow'), ('#ED46FF', 'pink')], default=None, max_length=18, null=True),
        ),
    ]
