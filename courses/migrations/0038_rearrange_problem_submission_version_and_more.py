# Generated by Django 4.0.3 on 2022-04-18 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0037_module_type_problem_non_editable_lines_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rearrange_problem_submission',
            name='version',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rearrange_problem_submission',
            name='status',
            field=models.BooleanField(default=0),
        ),
    ]
