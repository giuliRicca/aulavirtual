# Generated by Django 3.2 on 2021-05-28 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aula', '0007_auto_20210528_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]