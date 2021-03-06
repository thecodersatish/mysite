# Generated by Django 4.0.3 on 2022-04-03 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0027_alter_assignment_problem_submission_problem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment_Previous_Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.TextField(max_length=20000)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
