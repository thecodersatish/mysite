# Generated by Django 4.0.3 on 2022-04-12 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0034_quiz_submission_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz_submission',
            name='status',
            field=models.BooleanField(null=True),
        ),
    ]