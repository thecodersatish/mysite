# Generated by Django 4.0.3 on 2022-04-03 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0026_assignment_problem_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment_problem_submission',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.assignment_problem'),
        ),
    ]