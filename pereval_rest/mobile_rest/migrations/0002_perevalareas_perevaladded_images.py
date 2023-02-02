# Generated by Django 4.1.5 on 2023-02-02 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_rest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerevalAreas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mobile_rest.perevalareas')),
            ],
        ),
        migrations.CreateModel(
            name='PerevalAdded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_data', models.JSONField()),
                ('add_data', models.DateTimeField()),
                ('beautyTitle', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('other_titles', models.CharField(max_length=300)),
                ('connect', models.CharField(max_length=50)),
                ('add_time', models.DateTimeField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('height', models.IntegerField()),
                ('winter_level', models.CharField(max_length=5)),
                ('spring_level', models.CharField(max_length=5)),
                ('summer_level', models.CharField(max_length=5)),
                ('autumn_level', models.CharField(max_length=5)),
                ('status', models.CharField(max_length=10)),
                ('pereval_areas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mobile_rest.perevalareas')),
                ('tourist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mobile_rest.tourist')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.BinaryField()),
                ('pereval_added', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobile_rest.perevaladded')),
            ],
        ),
    ]