# Generated by Django 4.0.1 on 2022-03-17 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_alter_problem_submission_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem_submission',
            name='testcases_passed',
            field=models.IntegerField(default=0),
        ),
    ]
