# Generated by Django 4.0.3 on 2022-06-10 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0042_course_registration_batch_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='language_code',
            field=models.IntegerField(default=75),
        ),
    ]
