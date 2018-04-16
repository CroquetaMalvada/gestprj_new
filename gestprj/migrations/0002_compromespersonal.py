# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestprj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompromesPersonal',
            fields=[
                ('id_compromes', models.AutoField(serialize=False, primary_key=True, db_column='ID_COMPROMES')),
                ('id_projecte', models.DecimalField(null=True, decimal_places=0, max_digits=10, db_column='ID_PROJECTE', blank=True)),
                ('compte', models.CharField(max_length=15, null=True, db_column='COMPTE', blank=True)),
                ('descripcio', models.CharField(max_length=255, null=True, db_column='DESC', blank=True)),
                ('cost', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='COST', blank=True)),
                ('data_inici', models.DateField(null=True, db_column='DATA_INICI', blank=True)),
                ('data_fi', models.DateField(null=True, db_column='DATA_fI', blank=True)),
            ],
            options={
                'db_table': 'COMPROMES_PERSONAL',
                'managed': True,
            },
            bases=(models.Model,),
        ),
    ]
