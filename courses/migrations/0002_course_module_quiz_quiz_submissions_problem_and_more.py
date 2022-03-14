# Generated by Django 4.0.1 on 2022-02-21 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('img_url', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=250)),
                ('has_script', models.BooleanField()),
                ('script', models.CharField(blank=True, max_length=1000, null=True)),
                ('choice1', models.CharField(max_length=1000)),
                ('choice2', models.CharField(max_length=1000)),
                ('choice3', models.CharField(max_length=1000)),
                ('choice4', models.CharField(max_length=1000)),
                ('correct_choice', models.CharField(max_length=1000)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.module')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz_Submissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('option_selected', models.CharField(max_length=1000)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
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
        migrations.CreateModel(
            name='Previous_Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(max_length=18000)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course_Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(max_length=250)),
                ('no_of_questions_completed', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
