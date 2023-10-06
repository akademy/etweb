# Generated by Django 4.2.5 on 2023-10-05 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_species_wikimedia_photo_urls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detection',
            name='detector',
        ),
        migrations.AddField(
            model_name='analysis',
            name='detector',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='webapp.detector'),
            preserve_default=False,
        ),
    ]