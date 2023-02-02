# Generated by Django 4.1.5 on 2023-01-31 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tourist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=150, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('last_name', models.CharField(max_length=100)),
                ('patronymic', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
    ]