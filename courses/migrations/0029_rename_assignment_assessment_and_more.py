# Generated by Django 4.0.3 on 2022-04-03 14:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0028_assignment_previous_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Assignment',
            new_name='Assessment',
        ),
        migrations.RenameModel(
            old_name='Assignment_Previous_Code',
            new_name='Assessment_Previous_Code',
        ),
        migrations.RenameModel(
            old_name='Assignment_Problem',
            new_name='Assessment_Problem',
        ),
        migrations.RenameModel(
            old_name='Assignment_Problem_Submission',
            new_name='Assessment_Problem_Submission',
        ),
    ]
