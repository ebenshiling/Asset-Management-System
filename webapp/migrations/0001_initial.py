# Generated by Django 5.0.7 on 2024-07-22 15:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('asset_code', models.CharField(max_length=255, unique=True)),
                ('serial_number_t24', models.CharField(blank=True, default='NOT APPLICABLE', max_length=255, null=True)),
                ('nomenclature', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('date_purchase', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(max_length=10)),
                ('supplier', models.CharField(max_length=255)),
                ('warranty', models.CharField(choices=[('active', 'Active'), ('expired', 'Expired')], max_length=255)),
                ('comments', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='webapp.category')),
            ],
        ),
    ]