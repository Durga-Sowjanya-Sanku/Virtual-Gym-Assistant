# Generated by Django 5.0.6 on 2024-06-12 05:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('user_name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=15)),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('email', models.CharField(max_length=30)),
                ('mobile_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='exercise_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.CharField(max_length=30)),
                ('date_time', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('repetitions', models.IntegerField()),
                ('calories_burned', models.IntegerField()),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user_details')),
            ],
        ),
    ]
