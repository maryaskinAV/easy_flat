# Generated by Django 3.1 on 2022-02-24 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flat", "0005_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flat",
            name="avg_rating",
            field=models.FloatField(default=0, null=True),
        ),
    ]
