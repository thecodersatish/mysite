# Generated by Django 4.0.3 on 2022-06-16 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0043_course_language_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='rearrange_problem',
            name='statements',
            field=models.TextField(default='', max_length=20000),
        ),
    ]
