# Generated by Django 4.0.1 on 2022-01-07 09:15

import apps.queries.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='ssh_private_key',
            field=models.FileField(blank=True, null=True, upload_to=apps.queries.models.get_private_key),
        ),
    ]
