# Generated by Django 3.2.3 on 2021-07-05 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aula', '0019_auto_20210623_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]