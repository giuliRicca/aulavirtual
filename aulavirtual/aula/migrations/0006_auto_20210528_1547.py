# Generated by Django 3.2 on 2021-05-28 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aula', '0005_assignment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='subject',
        ),
        migrations.AddField(
            model_name='subject',
            name='assignments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aula.assignment'),
        ),
    ]