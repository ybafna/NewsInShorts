# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-21 19:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('getnews', '0006_news_source_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='source_id',
        ),
        migrations.AddField(
            model_name='news',
            name='source',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='getnews.Source'),
            preserve_default=False,
        ),
    ]
