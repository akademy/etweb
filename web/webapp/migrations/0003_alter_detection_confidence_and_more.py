# Generated by Django 4.2.5 on 2023-09-08 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_detection_confidence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detection',
            name='confidence',
            field=models.DecimalField(decimal_places=4, max_digits=5),
        ),
        migrations.AlterField(
            model_name='detector',
            name='description',
            field=models.TextField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='position',
            name='description',
            field=models.TextField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='species',
            name='description',
            field=models.TextField(max_length=4096),
        ),
    ]
