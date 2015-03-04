# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0003_auto_20150302_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmessagesmodel',
            name='cost',
            field=models.CharField(default='', max_length=20),
            preserve_default=True,
        ),
    ]
