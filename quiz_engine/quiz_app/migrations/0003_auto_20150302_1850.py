# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0002_auto_20150302_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentmessagesmodel',
            name='message',
            field=models.CharField(max_length=255, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membermodel',
            name='phone_number',
            field=models.CharField(max_length=20, default='', unique=True),
            preserve_default=True,
        ),
    ]
