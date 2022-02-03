# Generated by Django 3.2 on 2021-05-28 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aula', '0006_auto_20210528_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='assignments',
        ),
        migrations.AddField(
            model_name='assignment',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aula.subject'),
        ),
    ]