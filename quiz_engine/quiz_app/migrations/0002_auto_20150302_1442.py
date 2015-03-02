# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReceivedMessages',
            new_name='ReceivedMessagesModel',
        ),
    ]
