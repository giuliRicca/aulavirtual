# Generated by Django 3.2 on 2021-05-29 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aula', '0008_assignment_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assigment_file',
            field=models.FileField(blank=True, null=True, upload_to='documents/assigments/'),
        ),
    ]
