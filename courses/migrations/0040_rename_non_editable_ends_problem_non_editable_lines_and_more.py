# Generated by Django 4.0.3 on 2022-05-30 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0039_rename_non_editable_lines_problem_non_editable_ends_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='non_editable_ends',
            new_name='non_editable_lines',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='non_editable_starts',
        ),
    ]
