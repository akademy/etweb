# Generated by Django 4.2.5 on 2023-09-08 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_alter_analysis_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='detection',
            name='analysis',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webapp.analysis'),
            preserve_default=False,
        ),
    ]
