# Generated by Django 3.1 on 2021-12-23 10:55

import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rooms_count', models.SmallIntegerField()),
                ('cost', models.PositiveIntegerField()),
                ('comfortable', models.CharField(blank=True, max_length=200, null=True)),
                ('photos', models.ImageField(blank=True, null=True, upload_to='flat_images')),
                ('max_guest', models.SmallIntegerField()),
                ('arena_timeline', models.CharField(choices=[('OneDay', 'OneDay'), ('LongTime', 'LongTime'), ('Any', '')], max_length=200)),
                ('total_area', models.SmallIntegerField()),
                ('date_publisher', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Renting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_guest', models.PositiveIntegerField()),
                ('lease_duration', django.contrib.postgres.fields.ranges.DateRangeField()),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rent', to='flat.flat')),
            ],
        ),
    ]
