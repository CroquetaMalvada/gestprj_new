
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
# ESTO SIRVE PARA QUE EL AUTOFIELD PUEDA SER UN DECIMAL EN LUGAR DE UN INT
# from django.db.backends.mysql.creation import DatabaseCreation
# DatabaseCreation.data_types['AutoField'] = 'numeric(%(max_digits)s, %(decimal_places)s) AUTO_INCREMENT'
##############

from gestprj import pk
from django.contrib.auth.models import User

#
# class DesglossamentsPlantillPress(models.Model):
#     id_desglossament = models.DecimalField(db_column='ID_DESGLOSSAMENT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_partida_plantill = models.DecimalField(db_column='ID_PARTIDA_PLANTILL', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     compte = models.DecimalField(db_column='COMPTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_compte = models.DecimalField(db_column='ID_COMPTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_compte = models.CharField(db_column='DESC_COMPTE', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'DESGLOSSAMENTS_PLANTILL_PRESS'
#
#
#
#
#

#
#
#
#
#
# class PlantillaPressupost(models.Model):
#     id_partida_plantill = models.DecimalField(db_column='ID_PARTIDA_PLANTILL', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_plantilla = models.DecimalField(db_column='ID_PLANTILLA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_concepte_pres = models.DecimalField(db_column='ID_CONCEPTE_PRES', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'PLANTILLA_PRESSUPOST'
#
#
# class Plantilles(models.Model):
#     id_plantilla = models.DecimalField(db_column='ID_PLANTILLA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_plantilla = models.CharField(db_column='DESC_PLANTILLA', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'PLANTILLES'
#
#
# -------------------------------------------------------------------------




class TUsuarisXarxa(models.Model):
    id_usuari_xarxa = models.DecimalField(db_column='ID_USUARI_XARXA', max_digits=10, decimal_places=0, primary_key=True)  # Field name made lowercase.
    nom_xarxa = models.CharField(db_column='NOM_XARXA', max_length=255, blank=True)  # Field name made lowercase.
    id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True,unique=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_USUARIS_XARXA'

    def __unicode__( self ):
        return "{0} - {1}".format( self.id_usuari_xarxa, self.nom_xarxa )


class TOrganismes(models.Model):
    id_organisme = models.AutoField(db_column='ID_ORGANISME',primary_key=True)  #es necesario que el campo este como is identity en el servidor
    nom_organisme = models.CharField(db_column='NOM_ORGANISME', max_length=255, blank=True)  # Field name made lowercase.
    contacte = models.CharField(db_column='CONTACTE', max_length=255, blank=True)  # Field name made lowercase.
    adreca = models.CharField(db_column='ADRECA', max_length=255, blank=True)  # Field name made lowercase.
    cp = models.CharField(db_column='CP', max_length=255, blank=True)  # Field name made lowercase.
    poblacio = models.CharField(db_column='POBLACIO', max_length=255, blank=True)  # Field name made lowercase.
    provincia = models.CharField(db_column='PROVINCIA', max_length=255, blank=True)  # Field name made lowercase.
    pais = models.CharField(db_column='PAIS', max_length=255, blank=True)  # Field name made lowercase.
    tel1 = models.CharField(db_column='TEL1', max_length=255, blank=True)  # Field name made lowercase.
    tel2 = models.CharField(db_column='TEL2', max_length=255, blank=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=255, blank=True)  # Field name made lowercase.
    e_mail1 = models.CharField(db_column='E_MAIL1', max_length=255, blank=True)  # Field name made lowercase.
    e_mail2 = models.CharField(db_column='E_MAIL2', max_length=255, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_ORGANISMES'

    def __unicode__(self):
        return self.nom_organisme

class TCategoriaPrj(models.Model):
    id_categoria = models.DecimalField(db_column='ID_CATEGORIA', max_digits=10, decimal_places=0, blank=True,primary_key=True)  # Field name made lowercase.
    desc_categoria = models.CharField(db_column='DESC_CATEGORIA', max_length=255, blank=True)  # Field name made lowercase.
    serv_o_subven = models.CharField(db_column='SERV_O_SUBVEN', max_length=1, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_CATEGORIA_PRJ'

    def __unicode__(self):
        return self.desc_categoria

class TEstatPrj(models.Model):
    id_estat_prj = models.DecimalField(db_column='ID_ESTAT_PRJ', max_digits=10, decimal_places=0, blank=True,primary_key=True)  # Field name made lowercase.
    desc_estat_prj = models.CharField(db_column='DESC_ESTAT_PRJ', max_length=255, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_ESTAT_PRJ'

    def __unicode__(self):
        return self.desc_estat_prj

class TUsuarisCreaf(models.Model):
    #id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, primary_key=True)  # Field name made lowercase.
    #id_usuari = models.OneToOneField(TUsuarisXarxa,to_field="id_usuari",primary_key=True)
    # id_usuari = models.ForeignKey(TUsuarisXarxa,db_column='ID_USUARI',related_name="usuari_de",primary_key=True)
    id_usuari = models.AutoField(db_column='ID_USUARI',primary_key=True)
    nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
    adreca = models.CharField(db_column='ADRECA', max_length=255, blank=True)  # Field name made lowercase.
    cp = models.CharField(db_column='CP', max_length=255, blank=True)  # Field name made lowercase.
    poblacio = models.CharField(db_column='POBLACIO', max_length=255, blank=True)  # Field name made lowercase.
    provincia = models.CharField(db_column='PROVINCIA', max_length=255, blank=True)  # Field name made lowercase.
    pais = models.CharField(db_column='PAIS', max_length=255, blank=True)  # Field name made lowercase.
    tel1 = models.CharField(db_column='TEL1', max_length=255, blank=True)  # Field name made lowercase.
    tel2 = models.CharField(db_column='TEL2', max_length=255, blank=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=255, blank=True)  # Field name made lowercase.
    e_mail1 = models.CharField(db_column='E_MAIL1', max_length=255, blank=True)  # Field name made lowercase.
    e_mail2 = models.CharField(db_column='E_MAIL2', max_length=255, blank=True)  # Field name made lowercase.
    id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_USUARIS_CREAF'

class TUsuarisExterns(models.Model):
    id_usuari_extern = models.AutoField(db_column='ID_USUARI_EXTERN',primary_key=True)
    # id_usuari_extern = models.DecimalField(db_column='ID_USUARI_EXTERN', max_digits=10, decimal_places=0, blank=True,primary_key=True)  # puse primary key pero en hay projectos donde esta null!!!
    nom_usuari_extern = models.CharField(db_column='NOM_USUARI_EXTERN', max_length=255, blank=True)  # Field name made lowercase.
    # id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    adreca = models.CharField(db_column='ADRECA', max_length=255, blank=True)  # Field name made lowercase.
    cp = models.CharField(db_column='CP', max_length=255, blank=True)  # Field name made lowercase.
    poblacio = models.CharField(db_column='POBLACIO', max_length=255, blank=True)  # Field name made lowercase.
    provincia = models.CharField(db_column='PROVINCIA', max_length=255, blank=True)  # Field name made lowercase.
    pais = models.CharField(db_column='PAIS', max_length=255, blank=True)  # Field name made lowercase.
    tel1 = models.CharField(db_column='TEL1', max_length=255, blank=True)  # Field name made lowercase.
    tel2 = models.CharField(db_column='TEL2', max_length=255, blank=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=255, blank=True)  # Field name made lowercase.
    e_mail1 = models.CharField(db_column='E_MAIL1', max_length=255, blank=True)  # Field name made lowercase.
    e_mail2 = models.CharField(db_column='E_MAIL2', max_length=255, blank=True)  # Field name made lowercase.

    #FOREIGN KEYS
    id_organisme = models.ForeignKey(TOrganismes,related_name="organisme_de",db_column='ID_ORGANISME')

    class Meta:
        managed = False
        db_table = 'T_USUARIS_EXTERNS'

    def __unicode__(self):
        return "{0} ---- {1}".format(self.nom_usuari_extern,self.id_organisme)


class PersonalExtern(models.Model):
    id_perso_ext = models.AutoField(db_column='ID_PERSO_EXT',primary_key=True)  # Field name made lowercase.
    # id_perso_ext = models.DecimalField(db_column='ID_PERSO_EXT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_usuari_extern = models.DecimalField(db_column='ID_USUARI_EXTERN', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    #FOREIGN KEYS
    id_usuari_extern = models.ForeignKey(TUsuarisExterns,related_name="usuari_extern_de",db_column='ID_USUARI_EXTERN')

    class Meta:
        managed = False
        db_table = 'PERSONAL_EXTERN'




class Responsables(models.Model):
    id_resp = models.DecimalField(db_column='ID_RESP', max_digits=10, decimal_places=0, blank=True, primary_key=True)  # Field name made lowercase.
    codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    id_usuari = models.ForeignKey(TUsuarisCreaf,db_column='ID_USUARI')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RESPONSABLES'

    def __unicode__( self ):
        responsables = "{0} - {1}".format( self.codi_resp, self.id_usuari.nom_usuari )
        return responsables

class Projectes(models.Model):
    id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0,primary_key=True, )  # Quitado el pk.generaPkProjecte() porque solo se ejecuta una vez al iniciar el servidor
    #id_projecte = models.AutoField(db_column='ID_PROJECTE', primary_key=True, )  # Field name made lowercase.
    #id_resp = models.DecimalField(db_column='ID_RESP', max_digits=10, decimal_places=0)  # Field name made lowercase.
    codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
    codi_oficial = models.CharField(db_column='CODI_OFICIAL', max_length=255, blank=True)  # Field name made lowercase.
    titol = models.CharField(db_column='TITOL', max_length=255, blank=True)  # Field name made lowercase.
    acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
    resum = models.TextField(db_column='RESUM', blank=True)  # Field name made lowercase.
    comentaris = models.TextField(db_column='COMENTARIS', blank=True)  # Field name made lowercase.
    data_inici_prj = models.DateTimeField(db_column='DATA_INICI_PRJ', blank=True, null=True)  # Field name made lowercase.
    data_fi_prj = models.DateTimeField(db_column='DATA_FI_PRJ', blank=True, null=True)  # Field name made lowercase.
    # id_categoria = models.DecimalField(db_column='ID_CATEGORIA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    serv_o_subven = models.CharField(db_column='SERV_O_SUBVEN', max_length=1, blank=True) # Field name made lowercase.
    canon_oficial = models.DecimalField(db_column='CANON_OFICIAL', max_digits=17, decimal_places=2, blank=True, null=True,default=0)  # Field name made lowercase.
    percen_canon_creaf = models.DecimalField(db_column='PERCEN_CANON_CREAF', max_digits=7, decimal_places=4, blank=True, null=True,default=0)  # Field name made lowercase.
    percen_iva = models.DecimalField(db_column='PERCEN_IVA', max_digits=7, decimal_places=4, blank=True, null=True,default=0)  # Field name made lowercase.
    es_docum_web = models.CharField(db_column='ES_DOCUM_WEB', max_length=1, blank=True)  # Field name made lowercase.
    data_docum_web = models.DateField(db_column='DATA_DOCUM_WEB', blank=True, null=True)  # QUIZAS HAYA QUE USAR DATEFIELD!!!.
    # id_estat_prj = models.DecimalField(db_column='ID_ESTAT_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    es_coordinat = models.CharField(db_column='ES_COORDINAT', max_length=1, blank=True)  # Field name made lowercase.
    # id_usuari_extern = models.DecimalField(db_column='ID_USUARI_EXTERN', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    convocatoria = models.CharField(db_column='CONVOCATORIA', max_length=255, blank=True)  # Field name made lowercase.
    resolucio = models.CharField(db_column='RESOLUCIO', max_length=255, blank=True)  # Field name made lowercase.

    #MANY TO MANY
    usuaris_projecte = models.ManyToManyField(TUsuarisXarxa, through='PrjUsuaris')
    #organismes_projecte = models.ManyToManyField(TOrganismes, through='PrjUsuaris')
    centres_participants = models.ManyToManyField(TOrganismes, through='CentresParticipants')

    #FOREIGN KEYS
    id_resp = models.ForeignKey(Responsables,related_name="responsable_de",db_column='ID_RESP')
    id_categoria = models.ForeignKey(TCategoriaPrj,related_name="categoria_de",db_column='ID_CATEGORIA')
    id_estat_prj = models.ForeignKey(TEstatPrj,related_name="estat_de",db_column='ID_ESTAT_PRJ')
    id_usuari_extern = models.ForeignKey(TUsuarisExterns,related_name="extern_de",db_column='ID_USUARI_EXTERN',null=True, blank=True)


    class Meta:
        managed = False
        db_table = 'PROJECTES'


class PersonalCreaf(models.Model):
    id_perso_creaf = models.AutoField(db_column='ID_PERSO_CREAF',primary_key=True)  # Field name made lowercase.
    # id_perso_creaf = models.DecimalField(db_column='ID_PERSO_CREAF', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    es_justificacio = models.CharField(db_column='ES_JUSTIFICACIO', max_length=1, blank=True)  # Field name made lowercase.

    #FOREIGN KEYS
    id_projecte = models.ForeignKey(Projectes,related_name="projecte_de",db_column="ID_PROJECTE")
    id_usuari = models.ForeignKey(TUsuarisCreaf,related_name="usuari_de",db_column="ID_USUARI")

    class Meta:
        managed = False
        db_table = 'PERSONAL_CREAF'


class Renovacions(models.Model):
    id_renovacio = models.AutoField(db_column='ID_RENOVACIO', primary_key=True)  # Field name made lowercase.
    # id_renovacio = models.DecimalField(db_column='ID_RENOVACIO', max_digits=10, decimal_places=0, blank=True, primary_key=True)  # Field name made lowercase.
    # id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    data_inici = models.DateField(db_column='DATA_INICI', blank=True, null=True)  # Field name made lowercase.
    data_fi = models.DateField(db_column='DATA_FI', blank=True, null=True)  # Field name made lowercase.
    import_concedit = models.DecimalField(db_column='IMPORT_CONCEDIT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    #FOREIGN KEYS
    id_projecte = models.ForeignKey(Projectes,db_column="ID_PROJECTE")

    class Meta:
        managed = False
        db_table = 'RENOVACIONS'


class PrjUsuaris(models.Model):
    id_prj_usuaris = models.DecimalField(db_column='ID_PRJ_USUARIS', max_digits=10, decimal_places=0, blank=True, primary_key=True)  # Field name made lowercase.
    id_projecte = models.ForeignKey(Projectes,db_column='ID_PROJECTE')
    id_usuari_xarxa = models.ForeignKey(TUsuarisXarxa,db_column='ID_USUARI_XARXA')


    class Meta:
        managed = False
        db_table = 'PRJ_USUARIS'


class CentresParticipants(models.Model):
    id_centre_part = models.AutoField(db_column='ID_CENTRE_PART',primary_key=True) #es necesario que el campo este como is identity en el servidor
    # id_centre_part = models.DecimalField(db_column='ID_CENTRE_PART', max_digits=10, decimal_places=0, blank=True, primary_key=True)  # Field name made lowercase.
    #id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    id_projecte = models.ForeignKey(Projectes,db_column='ID_PROJECTE')
    #id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    id_organisme = models.ForeignKey(TOrganismes,db_column='ID_ORGANISME')

    class Meta:
        managed = False
        db_table = 'CENTRES_PARTICIPANTS'

class TFeines(models.Model):
    id_feina = models.AutoField(db_column='ID_FEINA', primary_key=True)  # Field name made lowercase.
    desc_feina = models.CharField(db_column='DESC_FEINA', max_length=255, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_FEINES'


class JustificPersonal(models.Model):
    id_justificacio = models.AutoField(db_column='ID_JUSTIFICACIO',primary_key=True)  # Field name made lowercase.
    # id_perso_creaf = models.DecimalField(db_column='ID_PERSO_CREAF', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    data_inici = models.DateField(db_column='DATA_INICI', blank=True, null=True)  # Field name made lowercase.
    data_fi = models.DateField(db_column='DATA_FI', blank=True, null=True)  # Field name made lowercase.
    # id_feina = models.DecimalField(db_column='ID_FEINA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    hores = models.DecimalField(db_column='HORES', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cost_hora = models.DecimalField(db_column='COST_HORA', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'JUSTIFIC_PERSONAL'

    #FOREIGN KEYS
    id_perso_creaf = models.ForeignKey(PersonalCreaf,db_column='ID_PERSO_CREAF')
    id_feina = models.ForeignKey(TFeines,db_column='ID_FEINA')

class JustificInternes(models.Model):
    id_justific_internes = models.AutoField(db_column='ID_JUSTIFIC_INTERNES', primary_key=True)  # Field name made lowercase.
    # id_justific_internes = models.DecimalField(db_column='ID_JUSTIFIC_INTERNES', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    data_assentament = models.DateField(db_column='DATA_ASSENTAMENT', blank=True, null=True)  # Field name made lowercase.
    id_assentament = models.DecimalField(db_column='ID_ASSENTAMENT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    desc_justif = models.CharField(db_column='DESC_JUSTIF', max_length=255, blank=True)  # Field name made lowercase.
    import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'JUSTIFIC_INTERNES'

    #FOREIGN KEYS
    id_projecte = models.ForeignKey(Projectes,db_column='ID_PROJECTE')

class Financadors(models.Model):
    id_financadors = models.AutoField(db_column='ID_FINANCADORS', primary_key=True)  # Field name made lowercase.
    # id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    import_concedit = models.DecimalField(db_column='IMPORT_CONCEDIT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FINANCADORS'

    #FOREIGN KEYS
    id_projecte = models.ForeignKey(Projectes,db_column='ID_PROJECTE')
    id_organisme = models.ForeignKey(TOrganismes,db_column='ID_ORGANISME')

class Receptors(models.Model):
    id_receptors = models.AutoField(db_column='ID_RECEPTORS', primary_key=True)  # Field name made lowercase.
    # id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    import_rebut = models.DecimalField(db_column='IMPORT_REBUT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RECEPTORS'

    #FOREIGN KEYS
    id_projecte = models.ForeignKey(Projectes,db_column='ID_PROJECTE')
    id_organisme = models.ForeignKey(TOrganismes,db_column='ID_ORGANISME')

class TConceptesPress(models.Model):
    id_concepte_pres = models.AutoField(db_column='ID_CONCEPTE_PRES', primary_key=True)  # Field name made lowercase.
    # id_concepte_pres = models.DecimalField(db_column='ID_CONCEPTE_PRES', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    desc_concepte = models.CharField(db_column='DESC_CONCEPTE', max_length=255, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_CONCEPTES_PRESS'


class Pressupost(models.Model):
    id_partida = models.AutoField(db_column='ID_PARTIDA', primary_key=True)  # Field name made lowercase.
    # id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_concepte_pres = models.DecimalField(db_column='ID_CONCEPTE_PRES', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.

    #FOREIGN KEYS
    id_projecte = models.ForeignKey(Projectes,db_column='ID_PROJECTE')
    id_concepte_pres = models.ForeignKey(TConceptesPress,db_column='ID_CONCEPTE_PRES')

    class Meta:
        managed = False
        db_table = 'PRESSUPOST'

class PeriodicitatPres(models.Model):
    id_periodicitat = models.AutoField(db_column='ID_PERIODICITAT', primary_key=True)  # Field name made lowercase.
    # id_periodicitat = models.DecimalField(db_column='ID_PERIODICITAT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    data_inicial = models.DateField(db_column='DATA_INICIAL', blank=True, null=True)  # Field name made lowercase.
    data_final = models.DateField(db_column='DATA_FINAL', blank=True, null=True)  # Field name made lowercase.
    etiqueta = models.CharField(db_column='ETIQUETA', max_length=255, blank=True)  # Field name made lowercase.

    #FOREIGN KEYS
    id_projecte = models.ForeignKey(Projectes,db_column='ID_PROJECTE')

    class Meta:
        managed = False
        db_table = 'PERIODICITAT_PRES'

class PeriodicitatPartida(models.Model):
    id_perio_partida = models.AutoField(db_column='ID_PERIO_PARTIDA', primary_key=True)  # Field name made lowercase.
    # id_perio_partida = models.DecimalField(db_column='ID_PERIO_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_periodicitat = models.DecimalField(db_column='ID_PERIODICITAT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.

    #FOREIGN KEYS
    id_partida = models.ForeignKey(Pressupost,db_column='ID_PARTIDA')
    id_periodicitat = models.ForeignKey(PeriodicitatPres,db_column='ID_PERIODICITAT')

    class Meta:
        managed = False
        db_table = 'PERIODICITAT_PARTIDA'

class ClausDiferenCompte(models.Model):
    id_compte = models.AutoField(db_column='ID_COMPTE', primary_key=True)  # Field name made lowercase.
    # id_compte = models.DecimalField(db_column='ID_COMPTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    clau_compte = models.CharField(db_column='CLAU_COMPTE', max_length=2, blank=True)  # Field name made lowercase.
    desc_clau = models.CharField(db_column='DESC_CLAU', max_length=255, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CLAUS_DIFEREN_COMPTE'

    def __unicode__( self ):
        comptes= "{0} - {1}".format( self.clau_compte, self.desc_clau )
        return comptes

class Desglossaments(models.Model):
    id_desglossament = models.AutoField(db_column='ID_DESGLOSSAMENT', primary_key=True)  # Field name made lowercase.
    # id_desglossament = models.DecimalField(db_column='ID_DESGLOSSAMENT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    compte = models.DecimalField(db_column='COMPTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_compte = models.DecimalField(db_column='ID_COMPTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    desc_compte = models.CharField(db_column='DESC_COMPTE', max_length=255, blank=True)  # Field name made lowercase.
    import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.

    #FOREIGN KEYS
    id_partida = models.ForeignKey(Pressupost,db_column='ID_PARTIDA')
    id_compte = models.ForeignKey(ClausDiferenCompte,db_column='ID_COMPTE',null=True,blank=True)



    class Meta:
        managed = False
        db_table = 'DESGLOSSAMENTS'



class JustificProjecte(models.Model):
    id_justificacio_prj = models.AutoField(db_column='ID_JUSTIFICACIO_PRJ', primary_key=True)  # Field name made lowercase.
    # id_justificacio_prj = models.DecimalField(db_column='ID_JUSTIFICACIO_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    data_justificacio = models.DateField(db_column='DATA_JUSTIFICACIO', blank=True, null=True)  # Field name made lowercase.
    data_inici_periode = models.DateField(db_column='DATA_INICI_PERIODE', blank=True, null=True)  # Field name made lowercase.
    data_fi_periode = models.DateField(db_column='DATA_FI_PERIODE', blank=True, null=True)  # Field name made lowercase.
    comentaris = models.TextField(db_column='COMENTARIS', blank=True)  # Field name made lowercase.

    #FOREIGN KEYS
    id_projecte = models.ForeignKey(Projectes,db_column='ID_PROJECTE')

    class Meta:
        managed = False
        db_table = 'JUSTIFIC_PROJECTE'


class AuditoriesProjecte(models.Model):
    id_auditoria_prj = models.AutoField(db_column='ID_AUDITORIA_PRJ', primary_key=True)  # Field name made lowercase.
    # id_auditoria_prj = models.DecimalField(db_column='ID_AUDITORIA_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    # id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    data_auditoria = models.DateField(db_column='DATA_AUDITORIA', blank=True, null=True)  # Field name made lowercase.
    data_inici_periode = models.DateField(db_column='DATA_INICI_PERIODE', blank=True, null=True)  # Field name made lowercase.
    data_fi_periode = models.DateField(db_column='DATA_FI_PERIODE', blank=True, null=True)  # Field name made lowercase.
    comentaris = models.TextField(db_column='COMENTARIS', blank=True)  # Field name made lowercase.

    #FOREIGN KEYS
    id_projecte = models.ForeignKey(Projectes,db_column='ID_PROJECTE')

    class Meta:
        managed = False
        db_table = 'AUDITORIES_PROJECTE'


#
#
#
#
# class UsuarisAdmin(models.Model):
#     id_usuari_admin = models.DecimalField(db_column='ID_USUARI_ADMIN', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_usuari_xarxa = models.DecimalField(db_column='ID_USUARI_XARXA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'USUARIS_ADMIN'
#
#
# class VAuditoriesPrj(models.Model):
#     id_auditoria_prj = models.DecimalField(db_column='ID_AUDITORIA_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     data_auditoria = models.DateTimeField(db_column='DATA_AUDITORIA', blank=True, null=True)  # Field name made lowercase.
#     data_inici_periode = models.DateTimeField(db_column='DATA_INICI_PERIODE', blank=True, null=True)  # Field name made lowercase.
#     data_fi_periode = models.DateTimeField(db_column='DATA_FI_PERIODE', blank=True, null=True)  # Field name made lowercase.
#     comentaris = models.TextField(db_column='COMENTARIS', blank=True)  # Field name made lowercase.
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#     id_estat_prj = models.DecimalField(db_column='ID_ESTAT_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_AUDITORIES_PRJ'
#
#
# class VCentresParticipants(models.Model):
#     id_centre_part = models.DecimalField(db_column='ID_CENTRE_PART', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     adreca = models.CharField(db_column='ADRECA', max_length=255, blank=True)  # Field name made lowercase.
#     contacte = models.CharField(db_column='CONTACTE', max_length=255, blank=True)  # Field name made lowercase.
#     cp = models.CharField(db_column='CP', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1 = models.CharField(db_column='E_MAIL1', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2 = models.CharField(db_column='E_MAIL2', max_length=255, blank=True)  # Field name made lowercase.
#     fax = models.CharField(db_column='FAX', max_length=255, blank=True)  # Field name made lowercase.
#     id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_organisme = models.CharField(db_column='NOM_ORGANISME', max_length=255, blank=True)  # Field name made lowercase.
#     pais = models.CharField(db_column='PAIS', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio = models.CharField(db_column='POBLACIO', max_length=255, blank=True)  # Field name made lowercase.
#     provincia = models.CharField(db_column='PROVINCIA', max_length=255, blank=True)  # Field name made lowercase.
#     tel1 = models.CharField(db_column='TEL1', max_length=255, blank=True)  # Field name made lowercase.
#     tel2 = models.CharField(db_column='TEL2', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_CENTRES_PARTICIPANTS'
#
#
# class VConcedit(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     concedit = models.DecimalField(db_column='CONCEDIT', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_CONCEDIT'
#
#
# class VDesglossaments(models.Model):
#     id_desglossament = models.DecimalField(db_column='ID_DESGLOSSAMENT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     compte = models.DecimalField(db_column='COMPTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_compte = models.DecimalField(db_column='ID_COMPTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     clau_compte = models.CharField(db_column='CLAU_COMPTE', max_length=2, blank=True)  # Field name made lowercase.
#     desc_clau = models.CharField(db_column='DESC_CLAU', max_length=255, blank=True)  # Field name made lowercase.
#     desc_compte = models.CharField(db_column='DESC_COMPTE', max_length=255, blank=True)  # Field name made lowercase.
#     import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
#
#     class Meta:
#         managed = False
#         db_table = 'V_DESGLOSSAMENTS'
#
#
# class VDesglossPlantillPress(models.Model):
#     id_desglossament = models.DecimalField(db_column='ID_DESGLOSSAMENT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     compte = models.DecimalField(db_column='COMPTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_compte = models.DecimalField(db_column='ID_COMPTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     clau_compte = models.CharField(db_column='CLAU_COMPTE', max_length=2, blank=True)  # Field name made lowercase.
#     desc_clau = models.CharField(db_column='DESC_CLAU', max_length=255, blank=True)  # Field name made lowercase.
#     desc_compte = models.CharField(db_column='DESC_COMPTE', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_DESGLOSS_PLANTILL_PRESS'
#
#
# class VFinancadors(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_financador = models.DecimalField(db_column='ID_FINANCADOR', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
#     adreca = models.CharField(db_column='ADRECA', max_length=255, blank=True)  # Field name made lowercase.
#     contacte = models.CharField(db_column='CONTACTE', max_length=255, blank=True)  # Field name made lowercase.
#     cp = models.CharField(db_column='CP', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1 = models.CharField(db_column='E_MAIL1', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2 = models.CharField(db_column='E_MAIL2', max_length=255, blank=True)  # Field name made lowercase.
#     fax = models.CharField(db_column='FAX', max_length=255, blank=True)  # Field name made lowercase.
#     id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_organisme = models.CharField(db_column='NOM_ORGANISME', max_length=255, blank=True)  # Field name made lowercase.
#     pais = models.CharField(db_column='PAIS', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio = models.CharField(db_column='POBLACIO', max_length=255, blank=True)  # Field name made lowercase.
#     provincia = models.CharField(db_column='PROVINCIA', max_length=255, blank=True)  # Field name made lowercase.
#     tel1 = models.CharField(db_column='TEL1', max_length=255, blank=True)  # Field name made lowercase.
#     tel2 = models.CharField(db_column='TEL2', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_FINANCADORS'
#
#
# class VJustificacionsPrj(models.Model):
#     id_justificacio_prj = models.DecimalField(db_column='ID_JUSTIFICACIO_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     data_justificacio = models.DateTimeField(db_column='DATA_JUSTIFICACIO', blank=True, null=True)  # Field name made lowercase.
#     data_inici_periode = models.DateTimeField(db_column='DATA_INICI_PERIODE', blank=True, null=True)  # Field name made lowercase.
#     data_fi_periode = models.DateTimeField(db_column='DATA_FI_PERIODE', blank=True, null=True)  # Field name made lowercase.
#     comentaris = models.TextField(db_column='COMENTARIS', blank=True)  # Field name made lowercase.
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#     id_estat_prj = models.DecimalField(db_column='ID_ESTAT_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_JUSTIFICACIONS_PRJ'
#
#
# class VJustificPersonal(models.Model):
#     cost_hora = models.DecimalField(db_column='COST_HORA', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#     data_fi = models.DateTimeField(db_column='DATA_FI', blank=True, null=True)  # Field name made lowercase.
#     data_inici = models.DateTimeField(db_column='DATA_INICI', blank=True, null=True)  # Field name made lowercase.
#     hores = models.DecimalField(db_column='HORES', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#     id_justificacio = models.DecimalField(db_column='ID_JUSTIFICACIO', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_perso_creaf = models.DecimalField(db_column='ID_PERSO_CREAF', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_feina = models.CharField(db_column='DESC_FEINA', max_length=255, blank=True)  # Field name made lowercase.
#     id_feina = models.DecimalField(db_column='ID_FEINA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_JUSTIFIC_PERSONAL'
#
#
# class VLlistaPrj(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     id_resp = models.DecimalField(db_column='ID_RESP', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_resp = models.CharField(db_column='NOM_RESP', max_length=255, blank=True)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#     titol = models.CharField(db_column='TITOL', max_length=255, blank=True)  # Field name made lowercase.
#     id_estat = models.DecimalField(db_column='ID_ESTAT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_estat = models.CharField(db_column='DESC_ESTAT', max_length=255, blank=True)  # Field name made lowercase.
#     data_alta = models.DateTimeField(db_column='DATA_ALTA', blank=True, null=True)  # Field name made lowercase.
#     canon_oficial = models.DecimalField(db_column='CANON_OFICIAL', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#     percen_canon_creaf = models.DecimalField(db_column='PERCEN_CANON_CREAF', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     percen_iva = models.DecimalField(db_column='PERCEN_IVA', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     concedit = models.DecimalField(db_column='CONCEDIT', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_LLISTA_PRJ'
#
#
# class VLlPresEtiquetes(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     id_resp = models.DecimalField(db_column='ID_RESP', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#     id_concepte_pres = models.DecimalField(db_column='ID_CONCEPTE_PRES', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_concepte = models.CharField(db_column='DESC_CONCEPTE', max_length=255, blank=True)  # Field name made lowercase.
#     id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
#     etiqueta = models.CharField(db_column='ETIQUETA', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_LL_PRES_ETIQUETES'
#
#
# class VLlPrjCategories(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#     id_estat_prj = models.DecimalField(db_column='ID_ESTAT_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#     id_categoria = models.DecimalField(db_column='ID_CATEGORIA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_categoria = models.CharField(db_column='DESC_CATEGORIA', max_length=255, blank=True)  # Field name made lowercase.
#     concedit = models.DecimalField(db_column='CONCEDIT', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_LL_PRJ_CATEGORIES'
#
#
# class VLlPrjFinancadors(models.Model):
#     id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_organisme = models.CharField(db_column='NOM_ORGANISME', max_length=255, blank=True)  # Field name made lowercase.
#     id_financadors = models.DecimalField(db_column='ID_FINANCADORS', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     import_concedit = models.DecimalField(db_column='IMPORT_CONCEDIT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#     id_estat_prj = models.DecimalField(db_column='ID_ESTAT_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_LL_PRJ_FINANCADORS'
#
#
# class VLlSelprjCatResp(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     serv_o_subven = models.CharField(db_column='SERV_O_SUBVEN', max_length=1, blank=True)  # Field name made lowercase.
#     id_categoria = models.DecimalField(db_column='ID_CATEGORIA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_categoria = models.CharField(db_column='DESC_CATEGORIA', max_length=255, blank=True)  # Field name made lowercase.
#     id_resp = models.DecimalField(db_column='ID_RESP', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_organisme = models.CharField(db_column='NOM_ORGANISME', max_length=255, blank=True)  # Field name made lowercase.
#     data_inici_prj = models.DateTimeField(db_column='DATA_INICI_PRJ', blank=True, null=True)  # Field name made lowercase.
#     data_fi_prj = models.DateTimeField(db_column='DATA_FI_PRJ', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_LL_SELPRJ_CAT_RESP'
#
#
# class VPartidesPrjPeriod(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_concepte_pres = models.DecimalField(db_column='ID_CONCEPTE_PRES', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_concepte = models.CharField(db_column='DESC_CONCEPTE', max_length=255, blank=True)  # Field name made lowercase.
#     id_periodicitat = models.DecimalField(db_column='ID_PERIODICITAT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     import_perio = models.DecimalField(db_column='IMPORT_PERIO', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PARTIDES_PRJ_PERIOD'
#
#
# class VPeriodicitatsPartida(models.Model):
#     id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_periodicitat = models.DecimalField(db_column='ID_PERIODICITAT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_perio_partida = models.DecimalField(db_column='ID_PERIO_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
#     data_final = models.DateTimeField(db_column='DATA_FINAL', blank=True, null=True)  # Field name made lowercase.
#     data_inicial = models.DateTimeField(db_column='DATA_INICIAL', blank=True, null=True)  # Field name made lowercase.
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PERIODICITATS_PARTIDA'
#
#
# class VPersonalCreaf(models.Model):
#     es_justificacio = models.CharField(db_column='ES_JUSTIFICACIO', max_length=1, blank=True)  # Field name made lowercase.
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_perso_creaf = models.DecimalField(db_column='ID_PERSO_CREAF', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     adreca = models.CharField(db_column='ADRECA', max_length=255, blank=True)  # Field name made lowercase.
#     cp = models.CharField(db_column='CP', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1 = models.CharField(db_column='E_MAIL1', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2 = models.CharField(db_column='E_MAIL2', max_length=255, blank=True)  # Field name made lowercase.
#     fax = models.CharField(db_column='FAX', max_length=255, blank=True)  # Field name made lowercase.
#     id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#     pais = models.CharField(db_column='PAIS', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio = models.CharField(db_column='POBLACIO', max_length=255, blank=True)  # Field name made lowercase.
#     provincia = models.CharField(db_column='PROVINCIA', max_length=255, blank=True)  # Field name made lowercase.
#     tel1 = models.CharField(db_column='TEL1', max_length=255, blank=True)  # Field name made lowercase.
#     tel2 = models.CharField(db_column='TEL2', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PERSONAL_CREAF'
#
#
# class VPersonalExtern(models.Model):
#     id_perso_ext = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     adreca_org = models.CharField(db_column='ADRECA_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     contacte_org = models.CharField(db_column='CONTACTE_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     cp_org = models.CharField(db_column='CP_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1_org = models.CharField(db_column='E_MAIL1_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2_org = models.CharField(db_column='E_MAIL2_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     fax_org = models.CharField(db_column='FAX_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     id_org = models.DecimalField(db_column='ID_ORG', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_org = models.CharField(db_column='NOM_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     pais_org = models.CharField(db_column='PAIS_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio_org = models.CharField(db_column='POBLACIO_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     provincia_org = models.CharField(db_column='PROVINCIA_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     tel1_org = models.CharField(db_column='TEL1_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     tel2_org = models.CharField(db_column='TEL2_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     adreca_user = models.CharField(db_column='ADRECA_USER', max_length=255, blank=True)  # Field name made lowercase.
#     cp_user = models.CharField(db_column='CP_USER', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1_user = models.CharField(db_column='E_MAIL1_USER', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2_user = models.CharField(db_column='E_MAIL2_USER', max_length=255, blank=True)  # Field name made lowercase.
#     fax_user = models.CharField(db_column='FAX_USER', max_length=255, blank=True)  # Field name made lowercase.
#     id_user = models.DecimalField(db_column='ID_USER', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_user = models.CharField(db_column='NOM_USER', max_length=255, blank=True)  # Field name made lowercase.
#     pais_user = models.CharField(db_column='PAIS_USER', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio_user = models.CharField(db_column='POBLACIO_USER', max_length=255, blank=True)  # Field name made lowercase.
#     provincia_user = models.CharField(db_column='PROVINCIA_USER', max_length=255, blank=True)  # Field name made lowercase.
#     tel1_user = models.CharField(db_column='TEL1_USER', max_length=255, blank=True)  # Field name made lowercase.
#     tel2_user = models.CharField(db_column='TEL2_USER', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PERSONAL_EXTERN'
#
#
# class VPersonalProjectesWeb(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     nom_treball = models.CharField(db_column='Nom_TREBALL', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PERSONAL_PROJECTES_WEB'
#
#
# class VPlantillaPressupost(models.Model):
#     id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_plantilla = models.DecimalField(db_column='ID_PLANTILLA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_concepte_pres = models.DecimalField(db_column='ID_CONCEPTE_PRES', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_concepte = models.CharField(db_column='DESC_CONCEPTE', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PLANTILLA_PRESSUPOST'
#
#
# class VPressupost(models.Model):
#     id_partida = models.DecimalField(db_column='ID_PARTIDA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
#     id_concepte_pres = models.DecimalField(db_column='ID_CONCEPTE_PRES', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     desc_concepte = models.CharField(db_column='DESC_CONCEPTE', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PRESSUPOST'
#
#
# class VProjectesServiceTonic(models.Model):
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#     responsable = models.CharField(db_column='RESPONSABLE', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PROJECTES_SERVICE_TONIC'
#
#
# class VProjectesUsuaris(models.Model):
#     id_prj_usuaris = models.DecimalField(db_column='ID_PRJ_USUARIS', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_usuari_xarxa = models.DecimalField(db_column='ID_USUARI_XARXA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_xarxa = models.CharField(db_column='NOM_XARXA', max_length=255, blank=True)  # Field name made lowercase.
#     id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     id_resp = models.DecimalField(db_column='ID_RESP', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PROJECTES_USUARIS'
#
#
# class VProjectesWeb(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     nom_responsable = models.CharField(db_column='NOM_RESPONSABLE', max_length=255, blank=True)  # Field name made lowercase.
#     codi_oficial = models.CharField(db_column='CODI_OFICIAL', max_length=255, blank=True)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#     titol = models.CharField(db_column='TITOL', max_length=255, blank=True)  # Field name made lowercase.
#     resum = models.TextField(db_column='RESUM', blank=True)  # Field name made lowercase.
#     comentaris = models.TextField(db_column='COMENTARIS', blank=True)  # Field name made lowercase.
#     data_inici_prj = models.DateTimeField(db_column='DATA_INICI_PRJ', blank=True, null=True)  # Field name made lowercase.
#     data_fi_prj = models.DateTimeField(db_column='DATA_FI_PRJ', blank=True, null=True)  # Field name made lowercase.
#     id_categoria = models.DecimalField(db_column='ID_CATEGORIA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     categoria = models.CharField(db_column='CATEGORIA', max_length=255, blank=True)  # Field name made lowercase.
#     estat_prj = models.CharField(db_column='ESTAT_PRJ', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_PROJECTES_WEB'
#
#
# class VReceptors(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_financador = models.DecimalField(db_column='ID_FINANCADOR', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     import_field = models.DecimalField(db_column='IMPORT', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
#     adreca = models.CharField(db_column='ADRECA', max_length=255, blank=True)  # Field name made lowercase.
#     contacte = models.CharField(db_column='CONTACTE', max_length=255, blank=True)  # Field name made lowercase.
#     cp = models.CharField(db_column='CP', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1 = models.CharField(db_column='E_MAIL1', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2 = models.CharField(db_column='E_MAIL2', max_length=255, blank=True)  # Field name made lowercase.
#     fax = models.CharField(db_column='FAX', max_length=255, blank=True)  # Field name made lowercase.
#     id_organisme = models.DecimalField(db_column='ID_ORGANISME', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_organisme = models.CharField(db_column='NOM_ORGANISME', max_length=255, blank=True)  # Field name made lowercase.
#     pais = models.CharField(db_column='PAIS', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio = models.CharField(db_column='POBLACIO', max_length=255, blank=True)  # Field name made lowercase.
#     provincia = models.CharField(db_column='PROVINCIA', max_length=255, blank=True)  # Field name made lowercase.
#     tel1 = models.CharField(db_column='TEL1', max_length=255, blank=True)  # Field name made lowercase.
#     tel2 = models.CharField(db_column='TEL2', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_RECEPTORS'
#
#
# class VResponsables(models.Model):
#     id_resp = models.DecimalField(db_column='ID_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     codi_resp = models.DecimalField(db_column='CODI_RESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_RESPONSABLES'
#
#
# class VUsuarisAdmin(models.Model):
#     id_usuari_admin = models.DecimalField(db_column='ID_USUARI_ADMIN', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     id_usuari_xarxa = models.DecimalField(db_column='ID_USUARI_XARXA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_xarxa = models.CharField(db_column='NOM_XARXA', max_length=255, blank=True)  # Field name made lowercase.
#     id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_USUARIS_ADMIN'
#
#
# class VUsuarisCreaf(models.Model):
#     id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#     adreca = models.CharField(db_column='ADRECA', max_length=255, blank=True)  # Field name made lowercase.
#     cp = models.CharField(db_column='CP', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio = models.CharField(db_column='POBLACIO', max_length=255, blank=True)  # Field name made lowercase.
#     provincia = models.CharField(db_column='PROVINCIA', max_length=255, blank=True)  # Field name made lowercase.
#     pais = models.CharField(db_column='PAIS', max_length=255, blank=True)  # Field name made lowercase.
#     tel1 = models.CharField(db_column='TEL1', max_length=255, blank=True)  # Field name made lowercase.
#     tel2 = models.CharField(db_column='TEL2', max_length=255, blank=True)  # Field name made lowercase.
#     fax = models.CharField(db_column='FAX', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1 = models.CharField(db_column='E_MAIL1', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2 = models.CharField(db_column='E_MAIL2', max_length=255, blank=True)  # Field name made lowercase.
#     id_org = models.DecimalField(db_column='ID_ORG', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_org = models.CharField(db_column='NOM_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     contacte_org = models.CharField(db_column='CONTACTE_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     adreca_org = models.CharField(db_column='ADRECA_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio_org = models.CharField(db_column='POBLACIO_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     provincia_org = models.CharField(db_column='PROVINCIA_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     pais_org = models.CharField(db_column='PAIS_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     cp_org = models.CharField(db_column='CP_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     tel1_org = models.CharField(db_column='TEL1_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     tel2_org = models.CharField(db_column='TEL2_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     fax_org = models.CharField(db_column='FAX_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1_org = models.CharField(db_column='E_MAIL1_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2_org = models.CharField(db_column='E_MAIL2_ORG', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_USUARIS_CREAF'
#
#
# class VUsuarisExterns(models.Model):
#     adreca_org = models.CharField(db_column='ADRECA_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     contacte_org = models.CharField(db_column='CONTACTE_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     cp_org = models.CharField(db_column='CP_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1_org = models.CharField(db_column='E_MAIL1_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2_org = models.CharField(db_column='E_MAIL2_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     fax_org = models.CharField(db_column='FAX_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     id_org = models.DecimalField(db_column='ID_ORG', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_org = models.CharField(db_column='NOM_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     pais_org = models.CharField(db_column='PAIS_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio_org = models.CharField(db_column='POBLACIO_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     provincia_org = models.CharField(db_column='PROVINCIA_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     tel1_org = models.CharField(db_column='TEL1_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     tel2_org = models.CharField(db_column='TEL2_ORG', max_length=255, blank=True)  # Field name made lowercase.
#     adreca_user = models.CharField(db_column='ADRECA_USER', max_length=255, blank=True)  # Field name made lowercase.
#     cp_user = models.CharField(db_column='CP_USER', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail1_user = models.CharField(db_column='E_MAIL1_USER', max_length=255, blank=True)  # Field name made lowercase.
#     e_mail2_user = models.CharField(db_column='E_MAIL2_USER', max_length=255, blank=True)  # Field name made lowercase.
#     fax_user = models.CharField(db_column='FAX_USER', max_length=255, blank=True)  # Field name made lowercase.
#     id_user = models.DecimalField(db_column='ID_USER', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_user = models.CharField(db_column='NOM_USER', max_length=255, blank=True)  # Field name made lowercase.
#     pais_user = models.CharField(db_column='PAIS_USER', max_length=255, blank=True)  # Field name made lowercase.
#     poblacio_user = models.CharField(db_column='POBLACIO_USER', max_length=255, blank=True)  # Field name made lowercase.
#     provincia_user = models.CharField(db_column='PROVINCIA_USER', max_length=255, blank=True)  # Field name made lowercase.
#     tel1_user = models.CharField(db_column='TEL1_USER', max_length=255, blank=True)  # Field name made lowercase.
#     tel2_user = models.CharField(db_column='TEL2_USER', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_USUARIS_EXTERNS'
#
#
# class VUsuarisXarxa(models.Model):
#     id_usuari_xarxa = models.DecimalField(db_column='ID_USUARI_XARXA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_xarxa = models.CharField(db_column='NOM_XARXA', max_length=255, blank=True)  # Field name made lowercase.
#     id_usuari = models.DecimalField(db_column='ID_USUARI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     nom_usuari = models.CharField(db_column='NOM_USUARI', max_length=255, blank=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'V_USUARIS_XARXA'
#
#
# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'
