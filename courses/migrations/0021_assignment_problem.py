# Generated by Django 4.0.3 on 2022-03-31 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_delete_assignment_problem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment_Problem',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=8000)),
                ('input_format', models.CharField(max_length=2000)),
                ('output_format', models.CharField(max_length=2000)),
                ('input1', models.CharField(max_length=500)),
                ('output1', models.CharField(max_length=500)),
                ('input2', models.CharField(max_length=500)),
                ('output2', models.CharField(max_length=500)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.module')),
            ],
        ),
    ]