# Generated by Django 4.0.3 on 2022-04-05 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0031_assessment_previous_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
    ]
