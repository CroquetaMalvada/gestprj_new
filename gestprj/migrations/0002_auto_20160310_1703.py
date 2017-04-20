# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestprj', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Projectes',
        ),
        migrations.CreateModel(
            name='Projectes',
            fields=[
            ],
            options={
                'db_table': 'PROJECTES',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
