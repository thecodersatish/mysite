# Generated by Django 4.0.3 on 2022-04-03 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0029_rename_assignment_assessment_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Assessment_Previous_Code',
        ),
    ]