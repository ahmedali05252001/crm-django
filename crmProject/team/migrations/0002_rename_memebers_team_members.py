# Generated by Django 5.0.1 on 2024-02-05 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='memebers',
            new_name='members',
        ),
    ]
