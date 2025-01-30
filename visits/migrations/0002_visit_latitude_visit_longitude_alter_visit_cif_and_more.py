# Generated by Django 5.1.4 on 2025-01-28 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='cif',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='visit',
            name='contract_number',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='visit',
            name='location',
            field=models.CharField(max_length=300),
        ),
    ]
