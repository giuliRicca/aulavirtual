# Generated by Django 3.2 on 2021-05-31 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aula', '0009_alter_assignment_assigment_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_file', models.FileField(upload_to='documents/assigments/')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aula.assignment')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='aula.student')),
            ],
        ),
    ]
