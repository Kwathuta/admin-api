# Generated by Django 3.2.9 on 2021-11-24 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employmentinformation',
            name='company',
        ),
    ]
