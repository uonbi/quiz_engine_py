# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MemberModel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(default='', max_length=50)),
                ('phone_number', models.CharField(default='', max_length=20)),
                ('quiz_count', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizModel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('question', models.CharField(default='', max_length=255)),
                ('answer', models.CharField(default='', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReceivedMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('phone_number', models.CharField(default='', max_length=20)),
                ('short_code', models.CharField(default='', max_length=10)),
                ('text', models.CharField(default='', max_length=255)),
                ('linkid', models.CharField(default='', max_length=255)),
                ('time_received', models.DateTimeField(help_text='The time the message was received at Africas Talking')),
                ('message_id', models.CharField(default='', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SentMessagesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('phone_number', models.CharField(default='', max_length=20)),
                ('short_code', models.CharField(default='', max_length=10, help_text='The shortcode that is used to reply the message')),
                ('status', models.CharField(default='', max_length=50, help_text='Store the status of the sent message')),
                ('message_id', models.CharField(default='', max_length=255)),
                ('cost', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubmissionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('answer', models.CharField(default='', max_length=50)),
                ('status', models.CharField(choices=[('C', 'Correct'), ('W', 'Wrong')], max_length=10)),
                ('quiz', models.ForeignKey(to='quiz_app.QuizModel')),
                ('user', models.ForeignKey(to='quiz_app.MemberModel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
