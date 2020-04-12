# Generated by Django 3.0.4 on 2020-04-12 05:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reciever_name',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='message',
            name='sender_name',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.date),
        ),
        migrations.AlterField(
            model_name='message',
            name='reciever_id',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender_id',
            field=models.UUIDField(),
        ),
    ]