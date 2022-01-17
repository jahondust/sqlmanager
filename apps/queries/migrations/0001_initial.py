# Generated by Django 4.0.1 on 2022-01-07 06:32

import apps.queries.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('mysql', 'MySQL'), ('postgresql', 'PostgreSQL')], default='postgresql', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('port', models.IntegerField()),
                ('db_name', models.CharField(max_length=255)),
                ('user_name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('use_ssh', models.BooleanField(default=False)),
                ('ssh_host', models.CharField(blank=True, max_length=255, null=True)),
                ('ssh_port', models.IntegerField(blank=True, null=True)),
                ('ssh_user_name', models.CharField(blank=True, max_length=255, null=True)),
                ('ssh_method', models.CharField(blank=True, max_length=255, null=True)),
                ('ssh_password', models.CharField(blank=True, max_length=255, null=True)),
                ('ssh_private_key', models.ImageField(blank=True, null=True, upload_to=apps.queries.models.get_private_key)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('query', models.CharField(blank=True, max_length=2000, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='queries', to='queries.category')),
                ('database', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='queries', to='queries.database')),
            ],
        ),
        migrations.CreateModel(
            name='Param',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('int', 'Integer'), ('float', 'Float'), ('text', 'Text'), ('date', 'Date'), ('datetime', 'DateTime')], default='text', max_length=255)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='params', to='queries.query')),
            ],
        ),
    ]
