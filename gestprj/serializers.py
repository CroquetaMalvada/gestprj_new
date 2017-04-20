from gestprj.models import CentresParticipants, TOrganismes, Projectes, TUsuarisExterns, PersonalExtern, TUsuarisCreaf, PersonalCreaf, JustificPersonal, TFeines, Financadors, Receptors, JustificInternes, Renovacions, TConceptesPress, Pressupost, PeriodicitatPres, PeriodicitatPartida, Desglossaments, ClausDiferenCompte, JustificProjecte, AuditoriesProjecte
from rest_framework import serializers
from gestprj import pk

class ProjectesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Projectes
        fields = ('url','id_projecte','titol')

# ORGANISMES #################
class GestTOrganismesSerializer(serializers.ModelSerializer): # info a obtener/mostrar

    class Meta:
        model = TOrganismes
        fields = ('url','id_organisme','nom_organisme','contacte','adreca','cp','poblacio','provincia','pais','tel1','tel2','fax','e_mail1','e_mail2')

# class GestTOrganismesSerializer(serializers.ModelSerializer): # datos necesarios para crear/editar
#
#     class Meta:
#         model = TOrganismes
#         fields = ('url','nom_organisme','contacte','adreca','cp','poblacio','provincia','pais','tel1','tel2','fax','e_mail1','e_mail2')


# CENTRES PARTICIPANTS #################
class GestCentresParticipantsSerializer(serializers.ModelSerializer):
    # id_organisme = serializers.DecimalField(max_digits=10, decimal_places=0, source='id_organisme.id_organisme', read_only=True)
    nom_organisme = serializers.CharField(source='id_organisme.nom_organisme', read_only=True)
    # id_projecte = serializers.DecimalField(max_digits=10, decimal_places=0, source='id_organisme.id_projecte', read_only=True)
    codi_oficial = serializers.CharField(source='id_projecte.codi_oficial', read_only=True)
    titol = serializers.CharField(source='id_projecte.titol', read_only=True)
    class Meta:
        model = CentresParticipants
        fields = ('url','id_organisme','nom_organisme','id_projecte','codi_oficial','titol')

# class GestCentreParticipantSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = CentresParticipants
#         fields = ('url','id_projecte','id_organisme')

# PERSONAL CREAF #################

class PersonalCreafSerializer(serializers.ModelSerializer):
    nom_usuari = serializers.CharField(source='id_usuari.nom_usuari', read_only=True)

    class Meta:
        model = PersonalCreaf
        fields = ('url','id_perso_creaf','id_projecte','id_usuari','nom_usuari','es_justificacio')


# USUARIS CREAF #################
class GestTUsuarisCreafSerializer(serializers.ModelSerializer): # info a obtener/mostrar

    class Meta:
        model = TUsuarisCreaf
        fields = ('url','id_usuari','nom_usuari','adreca','cp','poblacio','provincia','pais','tel1','tel2','fax','e_mail1','e_mail2','id_organisme')

# class GestTUsuarisCreafSerializer(serializers.ModelSerializer): # datos necesarios para crear/editar
#
#     class Meta:
#         model = TUsuarisCreaf
#         fields = ('url','nom_usuari','adreca','cp','poblacio','provincia','pais','tel1','tel2','fax','e_mail1','e_mail2','id_organisme')


# PERSONAL EXTERN #################
class PersonalExternSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalExtern
        fields = ('url','id_projecte','id_usuari_extern')

class PersonalExtern_i_organitzacioSerializer(serializers.ModelSerializer):
    nom_usuari_extern = serializers.CharField(source='id_usuari_extern.nom_usuari_extern', read_only=True)
    nom_organisme = serializers.CharField(source='id_usuari_extern.id_organisme.nom_organisme', read_only=True)

    class Meta:
        model = PersonalExtern
        fields = ('url','id_perso_ext','id_projecte','id_usuari_extern','nom_usuari_extern','nom_organisme')

# USUARIS EXTERNS #################
class TUsuarisExternsSerializer(serializers.ModelSerializer): # info a obtener/mostrar
    nom_organisme = serializers.CharField(source='id_organisme.nom_organisme', read_only=True)

    class Meta:
        model = TUsuarisExterns
        fields = ('url','id_usuari_extern','nom_usuari_extern','id_organisme','nom_organisme','adreca','cp','poblacio','provincia','pais','tel1','tel2','fax','e_mail1','e_mail2')

class GestTUsuarisExternsSerializer(serializers.ModelSerializer): # datos necesarios para crear/editar

    class Meta:
        model = TUsuarisExterns
        fields = ('url','nom_usuari_extern','adreca','cp','poblacio','provincia','pais','tel1','tel2','fax','e_mail1','e_mail2', 'id_organisme')

# JUSTIFICACIONS PERSONAL ##################

# class JustificPersonalSerializer(serializers.ModelSerializer): # info a obtener/mostrar
#     nom_feina = serializers.CharField(source='id_feina.desc_feina', read_only=True)
#     class Meta:
#         model = JustificPersonal
#         fields = ('url','data_inici','data_fi','nom_feina','hores','cost_hora')

class GestJustificPersonalSerializer(serializers.ModelSerializer): # info a obtener/mostrar
    nom_feina = serializers.CharField(source='id_feina.desc_feina', read_only=True)

    class Meta:
        model = JustificPersonal
        fields = ('url','id_perso_creaf','data_inici','data_fi','nom_feina','id_feina','hores','cost_hora')
# INTERNES
class GestJustifInternesSerializer(serializers.ModelSerializer): # info a obtener/mostrar
    class Meta:
        model = JustificInternes
        fields = ('url','id_projecte' ,'data_assentament','id_assentament','desc_justif','import_field')

# FINANCAMENT ######################

class GestOrganismesFinSerializer(serializers.ModelSerializer): # info a obtener/mostrar
    nom_organisme = serializers.CharField(source='id_organisme.nom_organisme', read_only=True)
    class Meta:
        model = Financadors
        fields = ('url','id_projecte','id_organisme','nom_organisme','import_concedit')

# RECEPTORS #####################
class GestOrganismesRecSerializer(serializers.ModelSerializer): # info a obtener/mostrar
    nom_organisme = serializers.CharField(source='id_organisme.nom_organisme', read_only=True)
    class Meta:
        model = Receptors
        fields = ('url','id_projecte','id_organisme','nom_organisme','import_rebut')

# RENOVACIONS (AKA CONCESSIONS DE DINERS) #####################

class GestRenovacionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renovacions
        fields = ('url','id_projecte','data_inici','data_fi','import_concedit')

# CONCEPTE PRESSUPOST (AKA PARTIDA) #####################

class GestConceptesPressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TConceptesPress
        fields = ('url','desc_concepte')

# PRESSUPOST ######################

class GestPressupostSerializer(serializers.ModelSerializer):
    nom_partida = serializers.CharField(source='id_concepte_pres.desc_concepte', read_only=True)
    id_part = serializers.DecimalField(max_digits=10, decimal_places=0, source='id_partida',read_only=True)
    class Meta:
        model = Pressupost
        fields =('url','id_part','id_projecte','id_concepte_pres','nom_partida','import_field')

# PERIODICITAT PRESSUPOST ############

class GestPeriodicitatPresSerializer(serializers.ModelSerializer):
    id_perio = serializers.DecimalField(max_digits=10, decimal_places=0, source='id_periodicitat',read_only=True)
    class Meta:
        model = PeriodicitatPres
        fields =('url','id_perio','id_projecte','data_inicial','data_final','etiqueta')
# PERIODICITAT PARTIDA ############

class GestPeriodicitatPartidaSerializer(serializers.ModelSerializer):
    data_inicial_perio = serializers.DateField(source='id_periodicitat.data_inicial', read_only=True)
    data_final_perio = serializers.DateField(source='id_periodicitat.data_final', read_only=True)

    class Meta:
        model = PeriodicitatPartida
        fields =('url','id_partida','id_periodicitat','import_field','data_inicial_perio','data_final_perio')

# DESGLOSSAMENT ############
class GestDesglossamentSerializer(serializers.ModelSerializer):
    clau = serializers.CharField(source='id_compte.clau_compte', read_only=True)
    class Meta:
        model = Desglossaments
        fields =('url','id_partida','compte','id_compte','clau','desc_compte','import_field')

# JUSTIFICACIONS PROJECTE ############
class GestJustificacionsProjecteSerializer(serializers.ModelSerializer):
    class Meta:
        model = JustificProjecte
        fields =('url','id_projecte','data_justificacio','data_inici_periode','data_fi_periode','comentaris')

# AUDITORIES ############
class GestAuditoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditoriesProjecte
        fields =('url','id_projecte','data_auditoria','data_inici_periode','data_fi_periode','comentaris')