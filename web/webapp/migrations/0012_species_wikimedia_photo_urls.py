# Generated by Django 4.2.5 on 2023-10-03 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_species_wikidata_url_species_wikimedia_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='wikimedia_photo_urls',
            field=models.URLField(default=None, max_length=1033),
            preserve_default=False,
        ),
    ]
