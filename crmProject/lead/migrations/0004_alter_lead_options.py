# Generated by Django 5.0.1 on 2024-02-05 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0003_lead_team'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lead',
            options={'ordering': ('name',)},
        ),
    ]