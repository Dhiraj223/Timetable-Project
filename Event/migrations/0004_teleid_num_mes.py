# Generated by Django 4.2.3 on 2023-07-24 14:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Event", "0003_teleid"),
    ]

    operations = [
        migrations.AddField(
            model_name="teleid",
            name="num_mes",
            field=models.CharField(default=1, max_length=200),
        ),
    ]
