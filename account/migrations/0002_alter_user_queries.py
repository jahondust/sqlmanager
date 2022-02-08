# Generated by Django 4.0.2 on 2022-02-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0008_alter_query_query'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='queries',
            field=models.ManyToManyField(blank=True, null=True, related_name='queries', to='queries.Query'),
        ),
    ]
