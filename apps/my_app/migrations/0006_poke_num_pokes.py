# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-25 04:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0005_poke'),
    ]

    operations = [
        migrations.AddField(
            model_name='poke',
            name='num_pokes',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
