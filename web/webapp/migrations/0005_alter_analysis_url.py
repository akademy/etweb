# Generated by Django 4.2.5 on 2023-09-08 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_analysis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='url',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
