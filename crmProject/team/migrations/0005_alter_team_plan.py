# Generated by Django 5.0.1 on 2024-02-08 09:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_team_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='team.plan'),
        ),
    ]
