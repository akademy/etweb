# Generated by Django 4.2.5 on 2023-10-03 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_alter_analysis_uuid_alter_detection_uuid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='wikidata_url',
            field=models.URLField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='species',
            name='wikimedia_url',
            field=models.URLField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='species',
            name='wikipedia_url',
            field=models.URLField(default=None, max_length=256),
            preserve_default=False,
        ),
    ]
