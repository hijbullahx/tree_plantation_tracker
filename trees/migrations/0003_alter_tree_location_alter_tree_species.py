# Generated by Django 4.2.23 on 2025-06-19 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trees", "0002_healthlog_death_reason_healthlog_is_dead_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tree",
            name="location",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="tree",
            name="species",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
