# Generated by Django 4.2.5 on 2023-09-08 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_alter_detection_confidence_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=4096)),
                ('url', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]