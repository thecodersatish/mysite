# Generated by Django 4.0.1 on 2022-02-21 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_rename_code_previous_code_source'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Previous_Code',
        ),
    ]
