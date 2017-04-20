# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projectes',
            fields=[
                ('id_projecte', models.DecimalField(serialize=False, decimal_places=0, primary_key=True, db_column='ID_PROJECTE', max_digits=10)),
                ('id_resp', models.DecimalField(decimal_places=0, max_digits=10, db_column='ID_RESP')),
                ('codi_prj', models.DecimalField(decimal_places=0, max_digits=10, db_column='CODI_PRJ')),
                ('codi_oficial', models.CharField(max_length=255, db_column='CODI_OFICIAL', blank=True)),
                ('titol', models.CharField(max_length=255, db_column='TITOL', blank=True)),
                ('acronim', models.CharField(max_length=255, db_column='ACRONIM', blank=True)),
                ('resum', models.TextField(db_column='RESUM', blank=True)),
                ('comentaris', models.TextField(db_column='COMENTARIS', blank=True)),
                ('data_inici_prj', models.DateTimeField(null=True, db_column='DATA_INICI_PRJ', blank=True)),
                ('data_fi_prj', models.DateTimeField(null=True, db_column='DATA_FI_PRJ', blank=True)),
                ('id_categoria', models.DecimalField(null=True, decimal_places=0, max_digits=10, db_column='ID_CATEGORIA', blank=True)),
                ('serv_o_subven', models.CharField(max_length=1, db_column='SERV_O_SUBVEN', blank=True)),
                ('canon_oficial', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='CANON_OFICIAL', blank=True)),
                ('percen_canon_creaf', models.DecimalField(null=True, decimal_places=4, max_digits=7, db_column='PERCEN_CANON_CREAF', blank=True)),
                ('percen_iva', models.DecimalField(null=True, decimal_places=4, max_digits=7, db_column='PERCEN_IVA', blank=True)),
                ('es_docum_web', models.CharField(max_length=1, db_column='ES_DOCUM_WEB', blank=True)),
                ('data_docum_web', models.DateTimeField(null=True, db_column='DATA_DOCUM_WEB', blank=True)),
                ('id_estat_prj', models.DecimalField(null=True, decimal_places=0, max_digits=10, db_column='ID_ESTAT_PRJ', blank=True)),
                ('es_coordinat', models.CharField(max_length=1, db_column='ES_COORDINAT', blank=True)),
                ('id_usuari_extern', models.DecimalField(null=True, decimal_places=0, max_digits=10, db_column='ID_USUARI_EXTERN', blank=True)),
                ('convocatoria', models.CharField(max_length=255, db_column='CONVOCATORIA', blank=True)),
                ('resolucio', models.CharField(max_length=255, db_column='RESOLUCIO', blank=True)),
            ],
            options={
                'db_table': 'PROJECTES',
            },
            bases=(models.Model,),
        ),
    ]
