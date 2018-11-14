# Generated by Django 2.1.2 on 2018-11-01 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calculation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=255)),
                ('source_lat', models.DecimalField(decimal_places=12, max_digits=20)),
                ('source_long', models.DecimalField(decimal_places=12, max_digits=20)),
                ('dest', models.CharField(max_length=255)),
                ('dest_lat', models.DecimalField(decimal_places=12, max_digits=20)),
                ('dest_long', models.DecimalField(decimal_places=12, max_digits=20)),
                ('uber_price', models.DecimalField(decimal_places=6, max_digits=10)),
                ('lyft_price', models.DecimalField(decimal_places=6, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_lat', models.DecimalField(decimal_places=12, max_digits=20)),
                ('start_long', models.DecimalField(decimal_places=12, max_digits=20)),
                ('end_lat', models.DecimalField(decimal_places=12, max_digits=20)),
                ('end_long', models.DecimalField(decimal_places=12, max_digits=20)),
            ],
        ),
    ]
