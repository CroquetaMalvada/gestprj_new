# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditoriesProjecte',
            fields=[
                ('id_auditoria_prj', models.AutoField(serialize=False, primary_key=True, db_column='ID_AUDITORIA_PRJ')),
                ('data_auditoria', models.DateField(null=True, db_column='DATA_AUDITORIA', blank=True)),
                ('data_inici_periode', models.DateField(null=True, db_column='DATA_INICI_PERIODE', blank=True)),
                ('data_fi_periode', models.DateField(null=True, db_column='DATA_FI_PERIODE', blank=True)),
                ('comentaris', models.TextField(db_column='COMENTARIS', blank=True)),
            ],
            options={
                'db_table': 'AUDITORIES_PROJECTE',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CentresParticipants',
            fields=[
                ('id_centre_part', models.AutoField(serialize=False, primary_key=True, db_column='ID_CENTRE_PART')),
            ],
            options={
                'db_table': 'CENTRES_PARTICIPANTS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClausDiferenCompte',
            fields=[
                ('id_compte', models.AutoField(serialize=False, primary_key=True, db_column='ID_COMPTE')),
                ('clau_compte', models.CharField(max_length=2, db_column='CLAU_COMPTE', blank=True)),
                ('desc_clau', models.CharField(max_length=255, db_column='DESC_CLAU', blank=True)),
            ],
            options={
                'db_table': 'CLAUS_DIFEREN_COMPTE',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Desglossaments',
            fields=[
                ('id_desglossament', models.AutoField(serialize=False, primary_key=True, db_column='ID_DESGLOSSAMENT')),
                ('compte', models.DecimalField(null=True, decimal_places=0, max_digits=10, db_column='COMPTE', blank=True)),
                ('desc_compte', models.CharField(max_length=255, db_column='DESC_COMPTE', blank=True)),
                ('import_field', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='IMPORT', blank=True)),
            ],
            options={
                'db_table': 'DESGLOSSAMENTS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Financadors',
            fields=[
                ('id_financadors', models.AutoField(serialize=False, primary_key=True, db_column='ID_FINANCADORS')),
                ('import_concedit', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='IMPORT_CONCEDIT', blank=True)),
            ],
            options={
                'db_table': 'FINANCADORS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JustificInternes',
            fields=[
                ('id_justific_internes', models.AutoField(serialize=False, primary_key=True, db_column='ID_JUSTIFIC_INTERNES')),
                ('data_assentament', models.DateField(null=True, db_column='DATA_ASSENTAMENT', blank=True)),
                ('id_assentament', models.DecimalField(null=True, decimal_places=0, max_digits=10, db_column='ID_ASSENTAMENT', blank=True)),
                ('desc_justif', models.CharField(max_length=255, db_column='DESC_JUSTIF', blank=True)),
                ('import_field', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='IMPORT', blank=True)),
            ],
            options={
                'db_table': 'JUSTIFIC_INTERNES',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JustificPersonal',
            fields=[
                ('id_justificacio', models.AutoField(serialize=False, primary_key=True, db_column='ID_JUSTIFICACIO')),
                ('data_inici', models.DateField(null=True, db_column='DATA_INICI', blank=True)),
                ('data_fi', models.DateField(null=True, db_column='DATA_FI', blank=True)),
                ('hores', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='HORES', blank=True)),
                ('cost_hora', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='COST_HORA', blank=True)),
            ],
            options={
                'db_table': 'JUSTIFIC_PERSONAL',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JustificProjecte',
            fields=[
                ('id_justificacio_prj', models.AutoField(serialize=False, primary_key=True, db_column='ID_JUSTIFICACIO_PRJ')),
                ('data_justificacio', models.DateField(null=True, db_column='DATA_JUSTIFICACIO', blank=True)),
                ('data_inici_periode', models.DateField(null=True, db_column='DATA_INICI_PERIODE', blank=True)),
                ('data_fi_periode', models.DateField(null=True, db_column='DATA_FI_PERIODE', blank=True)),
                ('comentaris', models.TextField(db_column='COMENTARIS', blank=True)),
            ],
            options={
                'db_table': 'JUSTIFIC_PROJECTE',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PeriodicitatPartida',
            fields=[
                ('id_perio_partida', models.AutoField(serialize=False, primary_key=True, db_column='ID_PERIO_PARTIDA')),
                ('import_field', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='IMPORT', blank=True)),
            ],
            options={
                'db_table': 'PERIODICITAT_PARTIDA',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PeriodicitatPres',
            fields=[
                ('id_periodicitat', models.AutoField(serialize=False, primary_key=True, db_column='ID_PERIODICITAT')),
                ('data_inicial', models.DateField(null=True, db_column='DATA_INICIAL', blank=True)),
                ('data_final', models.DateField(null=True, db_column='DATA_FINAL', blank=True)),
                ('etiqueta', models.CharField(max_length=255, db_column='ETIQUETA', blank=True)),
            ],
            options={
                'db_table': 'PERIODICITAT_PRES',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonalCreaf',
            fields=[
                ('id_perso_creaf', models.AutoField(serialize=False, primary_key=True, db_column='ID_PERSO_CREAF')),
                ('es_justificacio', models.CharField(max_length=1, db_column='ES_JUSTIFICACIO', blank=True)),
            ],
            options={
                'db_table': 'PERSONAL_CREAF',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonalExtern',
            fields=[
                ('id_perso_ext', models.AutoField(serialize=False, primary_key=True, db_column='ID_PERSO_EXT')),
                ('id_projecte', models.DecimalField(null=True, decimal_places=0, max_digits=10, db_column='ID_PROJECTE', blank=True)),
            ],
            options={
                'db_table': 'PERSONAL_EXTERN',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pressupost',
            fields=[
                ('id_partida', models.AutoField(serialize=False, primary_key=True, db_column='ID_PARTIDA')),
                ('import_field', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='IMPORT', blank=True)),
            ],
            options={
                'db_table': 'PRESSUPOST',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrjUsuaris',
            fields=[
                ('id_prj_usuaris', models.AutoField(serialize=False, primary_key=True, db_column='ID_PRJ_USUARIS')),
            ],
            options={
                'db_table': 'PRJ_USUARIS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Projectes',
            fields=[
                ('id_projecte', models.DecimalField(serialize=False, decimal_places=0, primary_key=True, db_column='ID_PROJECTE', max_digits=10)),
                ('codi_prj', models.DecimalField(decimal_places=0, max_digits=10, db_column='CODI_PRJ')),
                ('codi_oficial', models.CharField(max_length=255, db_column='CODI_OFICIAL', blank=True)),
                ('titol', models.CharField(max_length=255, db_column='TITOL', blank=True)),
                ('acronim', models.CharField(max_length=255, db_column='ACRONIM', blank=True)),
                ('resum', models.TextField(db_column='RESUM', blank=True)),
                ('comentaris', models.TextField(db_column='COMENTARIS', blank=True)),
                ('data_inici_prj', models.DateTimeField(null=True, db_column='DATA_INICI_PRJ', blank=True)),
                ('data_fi_prj', models.DateTimeField(null=True, db_column='DATA_FI_PRJ', blank=True)),
                ('serv_o_subven', models.CharField(max_length=1, db_column='SERV_O_SUBVEN', blank=True)),
                ('canon_oficial', models.DecimalField(db_column='CANON_OFICIAL', decimal_places=2, default=0, max_digits=17, blank=True, null=True)),
                ('percen_canon_creaf', models.DecimalField(db_column='PERCEN_CANON_CREAF', decimal_places=4, default=0, max_digits=7, blank=True, null=True)),
                ('percen_iva', models.DecimalField(db_column='PERCEN_IVA', decimal_places=4, default=0, max_digits=7, blank=True, null=True)),
                ('es_docum_web', models.CharField(max_length=1, db_column='ES_DOCUM_WEB', blank=True)),
                ('data_docum_web', models.DateField(null=True, db_column='DATA_DOCUM_WEB', blank=True)),
                ('es_coordinat', models.CharField(max_length=1, db_column='ES_COORDINAT', blank=True)),
                ('convocatoria', models.CharField(max_length=255, db_column='CONVOCATORIA', blank=True)),
                ('resolucio', models.CharField(max_length=255, db_column='RESOLUCIO', blank=True)),
            ],
            options={
                'db_table': 'PROJECTES',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Receptors',
            fields=[
                ('id_receptors', models.AutoField(serialize=False, primary_key=True, db_column='ID_RECEPTORS')),
                ('import_rebut', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='IMPORT_REBUT', blank=True)),
            ],
            options={
                'db_table': 'RECEPTORS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Renovacions',
            fields=[
                ('id_renovacio', models.AutoField(serialize=False, primary_key=True, db_column='ID_RENOVACIO')),
                ('data_inici', models.DateField(null=True, db_column='DATA_INICI', blank=True)),
                ('data_fi', models.DateField(null=True, db_column='DATA_FI', blank=True)),
                ('import_concedit', models.DecimalField(null=True, decimal_places=2, max_digits=17, db_column='IMPORT_CONCEDIT', blank=True)),
            ],
            options={
                'db_table': 'RENOVACIONS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Responsables',
            fields=[
                ('id_resp', models.AutoField(serialize=False, primary_key=True, db_column='ID_RESP')),
                ('codi_resp', models.DecimalField(null=True, decimal_places=0, max_digits=10, db_column='CODI_RESP', blank=True)),
            ],
            options={
                'db_table': 'RESPONSABLES',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TCategoriaPrj',
            fields=[
                ('id_categoria', models.DecimalField(primary_key=True, decimal_places=0, serialize=False, max_digits=10, blank=True, db_column='ID_CATEGORIA')),
                ('desc_categoria', models.CharField(max_length=255, db_column='DESC_CATEGORIA', blank=True)),
                ('serv_o_subven', models.CharField(max_length=1, db_column='SERV_O_SUBVEN', blank=True)),
            ],
            options={
                'db_table': 'T_CATEGORIA_PRJ',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TConceptesPress',
            fields=[
                ('id_concepte_pres', models.AutoField(serialize=False, primary_key=True, db_column='ID_CONCEPTE_PRES')),
                ('desc_concepte', models.CharField(max_length=255, db_column='DESC_CONCEPTE', blank=True)),
            ],
            options={
                'db_table': 'T_CONCEPTES_PRESS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TEstatPrj',
            fields=[
                ('id_estat_prj', models.DecimalField(primary_key=True, decimal_places=0, serialize=False, max_digits=10, blank=True, db_column='ID_ESTAT_PRJ')),
                ('desc_estat_prj', models.CharField(max_length=255, db_column='DESC_ESTAT_PRJ', blank=True)),
            ],
            options={
                'db_table': 'T_ESTAT_PRJ',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TFeines',
            fields=[
                ('id_feina', models.AutoField(serialize=False, primary_key=True, db_column='ID_FEINA')),
                ('desc_feina', models.CharField(max_length=255, db_column='DESC_FEINA', blank=True)),
            ],
            options={
                'db_table': 'T_FEINES',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TOrganismes',
            fields=[
                ('id_organisme', models.AutoField(serialize=False, primary_key=True, db_column='ID_ORGANISME')),
                ('nom_organisme', models.CharField(max_length=255, db_column='NOM_ORGANISME', blank=True)),
                ('contacte', models.CharField(max_length=255, db_column='CONTACTE', blank=True)),
                ('adreca', models.CharField(max_length=255, db_column='ADRECA', blank=True)),
                ('cp', models.CharField(max_length=255, db_column='CP', blank=True)),
                ('poblacio', models.CharField(max_length=255, db_column='POBLACIO', blank=True)),
                ('provincia', models.CharField(max_length=255, db_column='PROVINCIA', blank=True)),
                ('pais', models.CharField(max_length=255, db_column='PAIS', blank=True)),
                ('tel1', models.CharField(max_length=255, db_column='TEL1', blank=True)),
                ('tel2', models.CharField(max_length=255, db_column='TEL2', blank=True)),
                ('fax', models.CharField(max_length=255, db_column='FAX', blank=True)),
                ('e_mail1', models.CharField(max_length=255, db_column='E_MAIL1', blank=True)),
                ('e_mail2', models.CharField(max_length=255, db_column='E_MAIL2', blank=True)),
            ],
            options={
                'db_table': 'T_ORGANISMES',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TUsuarisCreaf',
            fields=[
                ('id_usuari', models.AutoField(serialize=False, primary_key=True, db_column='ID_USUARI')),
                ('nom_usuari', models.CharField(max_length=255, db_column='NOM_USUARI', blank=True)),
                ('adreca', models.CharField(max_length=255, db_column='ADRECA', blank=True)),
                ('cp', models.CharField(max_length=255, db_column='CP', blank=True)),
                ('poblacio', models.CharField(max_length=255, db_column='POBLACIO', blank=True)),
                ('provincia', models.CharField(max_length=255, db_column='PROVINCIA', blank=True)),
                ('pais', models.CharField(max_length=255, db_column='PAIS', blank=True)),
                ('tel1', models.CharField(max_length=255, db_column='TEL1', blank=True)),
                ('tel2', models.CharField(max_length=255, db_column='TEL2', blank=True)),
                ('fax', models.CharField(max_length=255, db_column='FAX', blank=True)),
                ('e_mail1', models.CharField(max_length=255, db_column='E_MAIL1', blank=True)),
                ('e_mail2', models.CharField(max_length=255, db_column='E_MAIL2', blank=True)),
                ('id_organisme', models.DecimalField(null=True, decimal_places=0, max_digits=10, db_column='ID_ORGANISME', blank=True)),
            ],
            options={
                'db_table': 'T_USUARIS_CREAF',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TUsuarisExterns',
            fields=[
                ('id_usuari_extern', models.AutoField(serialize=False, primary_key=True, db_column='ID_USUARI_EXTERN')),
                ('nom_usuari_extern', models.CharField(max_length=255, db_column='NOM_USUARI_EXTERN', blank=True)),
                ('adreca', models.CharField(max_length=255, db_column='ADRECA', blank=True)),
                ('cp', models.CharField(max_length=255, db_column='CP', blank=True)),
                ('poblacio', models.CharField(max_length=255, db_column='POBLACIO', blank=True)),
                ('provincia', models.CharField(max_length=255, db_column='PROVINCIA', blank=True)),
                ('pais', models.CharField(max_length=255, db_column='PAIS', blank=True)),
                ('tel1', models.CharField(max_length=255, db_column='TEL1', blank=True)),
                ('tel2', models.CharField(max_length=255, db_column='TEL2', blank=True)),
                ('fax', models.CharField(max_length=255, db_column='FAX', blank=True)),
                ('e_mail1', models.CharField(max_length=255, db_column='E_MAIL1', blank=True)),
                ('e_mail2', models.CharField(max_length=255, db_column='E_MAIL2', blank=True)),
            ],
            options={
                'db_table': 'T_USUARIS_EXTERNS',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TUsuarisXarxa',
            fields=[
                ('id_usuari_xarxa', models.DecimalField(serialize=False, decimal_places=0, primary_key=True, db_column='ID_USUARI_XARXA', max_digits=10)),
                ('nom_xarxa', models.CharField(max_length=255, db_column='NOM_XARXA', blank=True)),
                ('id_usuari', models.DecimalField(null=True, db_column='ID_USUARI', decimal_places=0, max_digits=10, blank=True, unique=True)),
            ],
            options={
                'db_table': 'T_USUARIS_XARXA',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
