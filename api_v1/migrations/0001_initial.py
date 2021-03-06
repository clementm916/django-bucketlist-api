# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 11:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucketlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bucketlists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_created',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('done', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, default='')),
                ('bucketlist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api_v1.Bucketlist')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('name', 'bucketlist_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='bucketlist',
            unique_together=set([('name', 'created_by')]),
        ),
    ]
