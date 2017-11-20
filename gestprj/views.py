from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connections
from django.core import serializers
from gestprj.models import Projectes, TCategoriaPrj, TOrganismes, CentresParticipants, PersonalExtern, TUsuarisExterns, PersonalCreaf, TUsuarisCreaf, JustificPersonal, TFeines, Financadors, Receptors, JustificInternes, Renovacions, TConceptesPress, Pressupost, PeriodicitatPres, PeriodicitatPartida, Desglossaments, ClausDiferenCompte, JustificProjecte, AuditoriesProjecte, Responsables, PrjUsuaris
from django.db.models import Q
from gestprj.forms import UsuariXarxaForm
from gestprj.forms import ProjectesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django_auth_ldap.config import LDAPGroupType
from gestprj.utils import usuari_a_responsable,id_resp_a_codi_responsable
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from gestprj.serializers import GestCentresParticipantsSerializer, ProjectesSerializer, \
    GestTOrganismesSerializer, PersonalExtern_i_organitzacioSerializer, \
    TUsuarisExternsSerializer, GestTUsuarisExternsSerializer, PersonalExternSerializer, PersonalCreafSerializer, \
    GestTUsuarisCreafSerializer, GestJustificPersonalSerializer, \
    GestOrganismesFinSerializer, GestOrganismesRecSerializer, GestJustifInternesSerializer, GestRenovacionsSerializer, \
    GestConceptesPressSerializer, GestPressupostSerializer, GestPeriodicitatPresSerializer, \
    GestPeriodicitatPartidaSerializer, GestDesglossamentSerializer, GestJustificacionsProjecteSerializer, \
    GestAuditoriesSerializer, GestPrjUsuarisSerializer
from gestprj import pk,contabilitat_ajax #,consultes_cont
from django.db import transaction
from datetime import datetime
from decimal import *
import json

# #funcion para comprovar si el usuario es admin o investigador
# def not_in_student_group(user):
#     """Use with a ``user_passes_test`` decorator to restrict access to
#     authenticated users who are not in the "Student" group."""
#     return user.groups.filter(name='Admins gestprj').exists()


###
def es_admin(user):
    return user.groups.filter(name="Admins gestprj").exists()

def es_usuario_valido(user):
    if user.groups.filter(name="Admins gestprj").exists() or user.groups.filter(name="Investigadors Principals").exists():
        return True
    else:
        return False
###


def dictfetchall(cursor):
    # Devuelve todos los campos de cada row como una lista
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# Create your views here.
@login_required(login_url='/menu/')
# @user_passes_test(lambda u: u.groups.filter(name="Admins gestprj").count() == 0, login_url="/logout/" )
def index(request):
    return HttpResponseRedirect('/llista_projectes/')
    # return HttpResponse("Hello, world.")


@login_required(login_url='/menu/')
@user_passes_test(es_admin,login_url='/contabilitat/')
def list_projectes(request): # poner ajax para funciones_datatables,pero no es nada urgente
    # llista_projectes = TUsuarisXarxa.objects.all()
    # usuarixarxa = usuari_xarxa_a_user(request)
    if request.user.groups.filter(name="Admins gestprj").exists():#si el usuario es un admin,muetra todos los proyectos
        llista_projectes = Projectes.objects.select_related('id_estat_prj').all()
    else:#sino solo muestra SUS proyectos
        responsable = usuari_a_responsable(request)

        if responsable is not None:
            llista_projectes = Projectes.objects.filter(id_resp__id_resp=responsable.id_resp)
        else:
            llista_projectes = None

    context = {'llista_projectes': llista_projectes, 'titulo': "LLISTA DE PROJECTES"}
    return render(request, 'gestprj/llista_projectes.html', context)

@login_required(login_url='/menu/')
@user_passes_test(es_admin,login_url='/welcome/')
def mod_project(request, id=None):
    categories = TCategoriaPrj.objects.all()
    organismes = TOrganismes.objects.all()
    feines = TFeines.objects.all()
    partides = TConceptesPress.objects.all()
    claus_comptes = ClausDiferenCompte.objects.all();
    nuevo = False
    try:
        instance = get_object_or_404(Projectes, id_projecte=id)
    except Http404:
        instance = None
        nuevo = True
        id = pk.generaPkProjecte()# Ojo al nombre de la bdd dentro de esta funcion!! Ademas pulirlo para evitar colisiones(aunque no deberia ya que vuelve a generarlo al guardarel prj por primera vez)

    form = ProjectesForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()  # \/ pasar el id por url no sirve,hay que ponerlo en la del form
        return render(request, 'gestprj/modificar_projecte.html',
                      {'form': form, 'titulo': 'EDITANT PROJECTE', 'categories': categories, 'organismes': organismes,
                       'tipus_feines': feines, 'partides': partides, 'claus_comptes': claus_comptes,
                       'id_projecte': id, 'guardado':True})  # , 'id_projecte':1534
    else:
        if nuevo:  # Si esta mal pero es nuevo( o si simplemente se clica en el boton "nou projecte" para empezar a crear uno )
            return render(request, 'gestprj/modificar_projecte.html',
                          {'form': form, 'titulo': 'NOU PROJECTE', 'categories': categories, 'organismes': organismes,
                           'tipus_feines': feines, 'partides': partides, 'claus_comptes': claus_comptes,
                           'id_projecte': id,
                           'nuevo': True})

    # Si esta mal pero se esta editando:(o se carga un proyecto)
    return render(request, 'gestprj/modificar_projecte.html',
                  {'form': form, 'titulo': 'EDITANT PROJECTE', 'categories': categories, 'organismes': organismes,
                   'tipus_feines': feines, 'partides': partides, 'claus_comptes': claus_comptes,
                   'id_projecte': id})


def login_view(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        # print username, password
        user = authenticate(username=username, password=password)
        if user is not None:#si el usuario es del creaf
            if (user.groups.filter(name="Admins gestprj").exists() or user.groups.filter(name="Investigadors Principals").exists()):# y ademas forma parte de alguno de los grupos necesarios
                login(request, user)
                return HttpResponseRedirect('/llista_projectes/', {'tipo': username})
            else:
                return render(request, 'gestprj/menu.html', {'username': username, 'errorpermis': True})
        else:
            return render(request, 'gestprj/menu.html', {'username': username, 'errorlogin': True})
    else:
        return render(request, 'gestprj/menu.html', {'username': ''})


def logout_view(request):
    logout(request)
    return render(request, 'gestprj/menu.html', {'username': ""})


# PROJECTES ######################
def ListProjectesSelect(request):  # AJAX
    resultado = contabilitat_ajax.AjaxListProjectesSelect()
    return HttpResponse(resultado, content_type='application/json;')


# USUARIS XARXA ######################
def ListUsuarisXarxaSelect(request):  # AJAX
    resultado = contabilitat_ajax.AjaxListUsuarisXarxaSelect()
    return HttpResponse(resultado, content_type='application/json;')


# CENTRES PARTICIPANTS #################
class CentresParticipantsViewSet(viewsets.ModelViewSet):  # todos los centros participantes
    queryset = CentresParticipants.objects.all()
    # queryset = CentresParticipants.objects.filter(id_projecte=)
    serializer_class = GestCentresParticipantsSerializer


class GestCentresParticipants(viewsets.ModelViewSet):  # gestionar centros participantes
    queryset = CentresParticipants.objects.all()
    serializer_class = GestCentresParticipantsSerializer


class ListCentresParticipantsProjecte(generics.ListAPIView):  # todos los centros participantes de un proyecto
    serializer_class = GestCentresParticipantsSerializer

    def get_queryset(self):
        _id_projecte = self.kwargs['id_projecte']
        return CentresParticipants.objects.filter(id_projecte=_id_projecte)

# ORGANISMES #################
def ListOrganismesSelect(request): # AJAX
    resultado = contabilitat_ajax.AjaxListOrganismesSelect()
    return HttpResponse(resultado, content_type='application/json;')

class ListTOrganismes(generics.ListAPIView):  # todos los organismos(usamos serializer ya que no es el  select y necesitaremos la url del serializer)
    serializer_class = GestTOrganismesSerializer

    def get_queryset(self):
        return TOrganismes.objects.all().order_by('nom_organisme')# .values("url","id_organisme", "nom_organisme")


class GestTOrganismes(viewsets.ModelViewSet):  # gestionar organismos
    queryset = TOrganismes.objects.all()
    serializer_class = GestTOrganismesSerializer


class ListTOrganismesNoProjecte(generics.ListAPIView):  # todos los organismos menos los del proyecto
    serializer_class = GestTOrganismesSerializer

    def get_queryset(self):
        _id_projecte = self.kwargs['id_projecte']
        if _id_projecte is None:
            return TOrganismes.objects.all()
        else:
            centres = CentresParticipants.objects.filter(id_projecte=_id_projecte)
            return TOrganismes.objects.exclude(id_organisme__in=centres.values_list('id_organisme'))

# PERSONAL CREAF #################

class ListPersonalCreafProjecte(generics.ListAPIView):
    serializer_class = PersonalCreafSerializer

    def get_queryset(self):
        _id_projecte = self.kwargs['id_projecte']
        return PersonalCreaf.objects.filter(id_projecte=_id_projecte)


class ListPersonalCreafNoProjecte(generics.ListAPIView):
    serializer_class = GestTUsuarisCreafSerializer

    def get_queryset(self):
        _id_projecte = self.kwargs['id_projecte']
        personal = PersonalCreaf.objects.filter(id_projecte=_id_projecte)
        return TUsuarisCreaf.objects.exclude(id_usuari__in=personal.values_list('id_usuari'))


class GestPersonalCreaf(viewsets.ModelViewSet):
    queryset = PersonalCreaf.objects.all()
    serializer_class = PersonalCreafSerializer


# USUARIS CREAF #################
class ListUsuarisCreaf(generics.ListAPIView):  # todos los organismos(usamos serializer ya que no es el  select y necesitaremos la url del serializer)
    serializer_class = GestTUsuarisCreafSerializer

    def get_queryset(self):
        return TUsuarisCreaf.objects.all().order_by('nom_usuari')

class GestTUsuarisCreaf(viewsets.ModelViewSet):
    queryset = TUsuarisCreaf.objects.all()
    serializer_class = GestTUsuarisCreafSerializer


# PERSONAL EXTERN #################
class ListPersonalExternProjecte(
    generics.ListAPIView):  # muestra los usuarios externos que participan en un proyecto junto con su organizacion
    serializer_class = PersonalExtern_i_organitzacioSerializer

    def get_queryset(self):
        _id_projecte = self.kwargs['id_projecte']
        return PersonalExtern.objects.filter(id_projecte=_id_projecte)


class ListPersonalExternNoProjecte(generics.ListAPIView):  # todos los usuarios externos menos los del proyecto
    serializer_class = TUsuarisExternsSerializer

    def get_queryset(self):
        _id_projecte = self.kwargs['id_projecte']
        personal = PersonalExtern.objects.filter(id_projecte=_id_projecte)
        return TUsuarisExterns.objects.exclude(id_usuari_extern__in=personal.values_list('id_usuari_extern'))


class GestPersonalExtern(viewsets.ModelViewSet):
    queryset = PersonalExtern.objects.all()
    serializer_class = PersonalExternSerializer


# USUARIS EXTERNS #################
class ListUsuarisExterns(generics.ListAPIView):  # todos los organismos(usamos serializer ya que no es el  select y necesitaremos la url del serializer)
    serializer_class = TUsuarisExternsSerializer

    def get_queryset(self):
        return TUsuarisExterns.objects.all().order_by('nom_usuari_extern')

class GestTUsuarisExterns(viewsets.ModelViewSet):  # todos los usuarios externos
    queryset = TUsuarisExterns.objects.all()
    serializer_class = GestTUsuarisExternsSerializer


# PROJECTES #################
class ProjectesViewSet(viewsets.ModelViewSet):
    queryset = Projectes.objects.all()
    serializer_class = ProjectesSerializer


# JUSTIFICACIONS #########
# PERSONAL


class ListJustificPersonal(generics.ListAPIView):  # las justificaciones de cierto usuario creaf
    serializer_class = GestJustificPersonalSerializer

    def get_queryset(self):
        _id_perso = self.kwargs['id_personal']
        return JustificPersonal.objects.filter(id_perso_creaf=_id_perso)


class GestJustificPersonal(viewsets.ModelViewSet):
    queryset = JustificPersonal.objects.all()
    serializer_class = GestJustificPersonalSerializer



################## FINANCAMENT

# ORGANISMES FINANCADORS

class ListOrganismesFin(generics.ListAPIView):
    serializer_class = GestOrganismesFinSerializer

    def get_queryset(self):
        if self.kwargs['id_projecte'] is None:
            return Financadors.objects.all()
        else:
            _id_projecte = self.kwargs['id_projecte']
            return Financadors.objects.filter(id_projecte=_id_projecte)


class GestOrganismesFin(viewsets.ModelViewSet):
    queryset = Financadors.objects.all()
    serializer_class = GestOrganismesFinSerializer


# ORGANISMES RECEPTORS

class ListOrganismesRec(generics.ListAPIView):
    serializer_class = GestOrganismesRecSerializer

    def get_queryset(self):
        if self.kwargs['id_projecte'] is None:
            return Receptors.objects.all()
        else:
            _id_projecte = self.kwargs['id_projecte']
            return Receptors.objects.filter(id_projecte=_id_projecte)


class GestOrganismesRec(viewsets.ModelViewSet):
    queryset = Receptors.objects.all()
    serializer_class = GestOrganismesRecSerializer


# JUSTIFICACIONS INTERNES

class ListJustifInternes(generics.ListAPIView):
    serializer_class = GestJustifInternesSerializer

    def get_queryset(self):
        if self.kwargs['id_projecte'] is None:
            return JustificInternes.objects.all()
        else:
            _id_projecte = self.kwargs['id_projecte']
            return JustificInternes.objects.filter(id_projecte=_id_projecte)


class GestJustifInternes(viewsets.ModelViewSet):
    queryset = JustificInternes.objects.all()
    serializer_class = GestJustifInternesSerializer


# RENOVACIONS (AKA CONCESSIONS DE DINERS)

class ListRenovacions(generics.ListAPIView):
    serializer_class = GestRenovacionsSerializer

    def get_queryset(self):
        if self.kwargs['id_projecte'] is None:
            return Renovacions.objects.all()
        else:
            _id_projecte = self.kwargs['id_projecte']
            return Renovacions.objects.filter(id_projecte=_id_projecte)


class GestRenovacions(viewsets.ModelViewSet):

    queryset = Renovacions.objects.all()
    serializer_class = GestRenovacionsSerializer


# CONCEPTE PRESSUPOST (AKA PARTIDA

def ListConceptesPress(request):

    conceptos = TConceptesPress.objects.all().order_by('desc_concepte')
    resultado=[]
    for concepte in conceptos:
        resultado.append({'id':str(concepte.id_concepte_pres),'descripcio': concepte.desc_concepte})

    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

class GestConceptesPress(viewsets.ModelViewSet):
    queryset = TConceptesPress.objects.all()
    serializer_class = GestConceptesPressSerializer


# PRESSUPOST

class ListPressupost(generics.ListAPIView):
    serializer_class = GestPressupostSerializer

    def get_queryset(self):
        if self.kwargs['id_projecte'] is None:
            return Pressupost.objects.all()
        else:
            _id_projecte = self.kwargs['id_projecte']
            return Pressupost.objects.filter(id_projecte=_id_projecte)


class GestPressupost(viewsets.ModelViewSet):
    queryset = Pressupost.objects.all()
    serializer_class = GestPressupostSerializer


# PERIODICITAT PRESSUPOST

class ListPeriodicitatPres(generics.ListCreateAPIView):
    serializer_class = GestPeriodicitatPresSerializer

    def get_queryset(self):
        if self.kwargs['id_projecte'] is None:
            return PeriodicitatPres.objects.all()
        else:
            _id_projecte = self.kwargs['id_projecte']
            return PeriodicitatPres.objects.filter(id_projecte=_id_projecte)


class GestPeriodicitatPres(viewsets.ModelViewSet):
    queryset = PeriodicitatPres.objects.all()
    serializer_class = GestPeriodicitatPresSerializer


# PERIODICITAT PARTIDA

class ListPeriodicitatPartida(generics.ListCreateAPIView):
    serializer_class = GestPeriodicitatPartidaSerializer

    def get_queryset(self):
        if self.kwargs['id_partida'] is None:
            return PeriodicitatPartida.objects.all()
        else:
            _id_partida = self.kwargs['id_partida']
            return PeriodicitatPartida.objects.filter(id_partida=_id_partida)



class GestPeriodicitatPartida(viewsets.ModelViewSet):
    queryset = PeriodicitatPartida.objects.all()
    serializer_class = GestPeriodicitatPartidaSerializer


# DESGLOSSAMENT

class ListDesglossament(generics.ListCreateAPIView):
    serializer_class = GestDesglossamentSerializer

    def get_queryset(self):
        if self.kwargs['id_partida'] is None:
            return Desglossaments.objects.all()
        else:
            _id_partida = self.kwargs['id_partida']
            return Desglossaments.objects.filter(id_partida=_id_partida)



class GestDesglossament(viewsets.ModelViewSet):
    queryset = Desglossaments.objects.all()
    serializer_class = GestDesglossamentSerializer


# JUSTIFICACIONS DEL PROJECTE

class ListJustificacionsProjecte(generics.ListCreateAPIView):
    serializer_class = GestJustificacionsProjecteSerializer

    def get_queryset(self):
        if self.kwargs['id_projecte'] is None:
            return JustificProjecte.objects.all()
        else:
            _id_projecte = self.kwargs['id_projecte']
            return JustificProjecte.objects.filter(id_projecte=_id_projecte)


class GestJustificacionsProjecte(viewsets.ModelViewSet):
    queryset = JustificProjecte.objects.all()
    serializer_class = GestJustificacionsProjecteSerializer


# AUDITORIES DEL PROJECTE

class ListAuditories(generics.ListCreateAPIView):
    serializer_class = GestAuditoriesSerializer

    def get_queryset(self):
        if self.kwargs['id_projecte'] is None:
            return AuditoriesProjecte.objects.all()
        else:
            _id_projecte = self.kwargs['id_projecte']
            return AuditoriesProjecte.objects.filter(id_projecte=_id_projecte)


class GestAuditories(viewsets.ModelViewSet):
    queryset = AuditoriesProjecte.objects.all()
    serializer_class = GestAuditoriesSerializer


# PERMISOS DE USUARIOS PARA CONSULTAR OTROS PROYECTOS#################
class ListPermisosUsuarisConsultar(generics.ListAPIView):  # usamos serializer ya que no es el  select y necesitaremos la url del serializer)
    serializer_class = GestPrjUsuarisSerializer

    def get_queryset(self):
        return PrjUsuaris.objects.all() # order_by('nom_xarxa')

class GestPrjUsuaris(viewsets.ModelViewSet):
    queryset = PrjUsuaris.objects.all()
    serializer_class = GestPrjUsuarisSerializer

################################ CONTABILIDAD!!!!

# VERSION CONTABILIDAD
def json_vacio(request):
    return HttpResponse([{}], content_type='application/json;')

@login_required(login_url='/menu/')
def list_projectes_cont(request): #simplemente carga la template
    context = { 'titulo': "CONTABILITAT"} # 'llista_projectes': llista_projectes ,
    return render(request, 'gestprj/contabilitat.html', context)

#AJAX PARA RELLENAR RESPONSABLES
@login_required(login_url='/menu/')
def ListResponsablesCont(request):
    resultado=contabilitat_ajax.AjaxListResponsablesCont(request)
    return HttpResponse(resultado, content_type='application/json;')


#AJAX PARA RELLENAR PROYECTOS
@login_required(login_url='/menu/')
def ListProjectesCont(request):

    resultado = contabilitat_ajax.AjaxListProjectesCont(request)
    return HttpResponse(resultado, content_type='application/json;')


# DADES PROJECTE

@login_required(login_url='/menu/')
def cont_dades(request):

    projectes = request.POST

    resultado = []
    for projecte_chk in projectes.getlist("prj_select"):

        ##### Para extraer el objeto proyecto:
        cod_responsable = projecte_chk.split("-")[0]
        id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
        cod_projecte = projecte_chk.split("-")[1]
        projecte = Projectes.objects.get(codi_prj=cod_projecte,
                                         id_resp=id_resp)  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj

        # if int(cod_responsable) < 10:
        #     cod_responsable="0"+str(cod_responsable)
        # if int(cod_projecte) < 100:
        #     if int(cod_projecte) < 10:
        #         cod_projecte="00"+str(cod_projecte)
        #     else:
        #         cod_projecte="0"+str(cod_projecte)
        if len(cod_responsable) < 2:
            cod_responsable = "0" + str(cod_responsable)
        if len(cod_projecte) < 3:
            if len(cod_projecte) < 2:
                cod_projecte = "00" + str(cod_projecte)
            else:
                cod_projecte = "0" + str(cod_projecte)

        #####
        centres_participants = CentresParticipants.objects.filter(id_projecte=projecte.id_projecte)
        participants_creaf = PersonalCreaf.objects.filter(id_projecte=projecte.id_projecte)
        participants_externs = PersonalExtern.objects.filter(id_projecte=projecte.id_projecte)

        financadors = Financadors.objects.filter(id_projecte=projecte.id_projecte)
        receptors = Receptors.objects.filter(id_projecte=projecte.id_projecte)

        # CANON I IVA
        concedit = 0
        for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
            concedit = round(concedit + float(importe.import_concedit), 2)
        # vienen en la tabla:
        percen_iva = round(projecte.percen_iva, 2)
        percen_canon_creaf = round(projecte.percen_canon_creaf, 2)
        canon_oficial = round(projecte.canon_oficial, 2)

        # calculados a mano
        if concedit == 0:  # para evitar problemas con la division si es 0
            percen_canon_oficial = 0.00
        else:
            percen_canon_oficial = round(((canon_oficial / concedit) * (100 * (1 + percen_iva / 100))), 2)
        canon_creaf = round(((concedit * percen_canon_creaf) / (100 * (1 + percen_iva / 100))), 2)
        diferencia_per = round((percen_canon_oficial - percen_canon_creaf), 2)
        diferencia_eur = round((canon_oficial - canon_creaf), 2)
        iva = round(((concedit * percen_iva) / (100 * (1 + percen_iva / 100))), 2)

        canoniva = {"percen_iva": percen_iva, "percen_canon_creaf": percen_canon_creaf, "canon_oficial": canon_oficial,
                    "percen_canon_oficial": percen_canon_oficial, "canon_creaf": canon_creaf,
                    "diferencia_per": diferencia_per, "diferencia_eur": diferencia_eur, "iva": iva}
        ####

        # DESPESES
        despeses = []
        despesa_total_concedit = 0
        despesa_total_iva = 0
        despesa_total_canon = 0
        despesa_total_net = 0
        for despesa in Renovacions.objects.filter(id_projecte=projecte.id_projecte):
            import_concedit = float(despesa.import_concedit)
            despesa_total_concedit = despesa_total_concedit + import_concedit
            iva = round(((import_concedit * percen_iva) / 100), 2)
            despesa_total_iva = despesa_total_iva + iva
            canon = round(((import_concedit * percen_canon_creaf) / 100), 2)
            despesa_total_canon = despesa_total_canon + canon
            net = round((import_concedit - iva - canon), 2)
            despesa_total_net = despesa_total_net + net
            despeses.append(
                {"data_inici": despesa.data_inici, "data_fi": despesa.data_fi, "concedit": import_concedit, "iva": iva,
                 "canon": canon, "net": net})
            # concedit = round(concedit + float(importe.import_concedit),2)

            ####

            # PRESSUPOST
        partides = []
        max_periodes = 0;
        # al suma de cada periodo
        totals = [0, 0, 0, 0, 0, 0, 0, 0]
        total_import = 0
        partida_total = 0

        # primero vemos cual es el max de periodos que tiene una de als partidas
        for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
            n_periodes = 0
            for periode in PeriodicitatPartida.objects.filter(id_partida=partida.id_partida):
                n_periodes = n_periodes + 1
                if n_periodes > max_periodes:
                    max_periodes = n_periodes
        ######

        # Despues ponesmos los periodos en cada partida,usamos el max anterior para rellenar con 0 en caso de que haya menos periodos que el maximo
        for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
            periodes = []
            total_periode = 0

            for index, periode in enumerate(PeriodicitatPartida.objects.filter(id_partida=partida.id_partida)):
                total_periode = total_periode + periode.import_field
                totals[index] = totals[index] + periode.import_field
                periodes.append({"importe": periode.import_field})

            if len(periodes) < max_periodes:
                for dif in range((max_periodes - len(periodes))):
                    periodes.append({"importe": 0.00})

            totals[max_periodes] = totals[max_periodes] + total_periode

            ######

            # Si no hay periodos,comprovar si las propias partidas tienen importe:
            if not periodes:
                total_import = total_import + partida.import_field
                partides.append({"concepte": partida.id_concepte_pres.desc_concepte, "import": partida.import_field})
            else:
                partides.append(
                    {"concepte": partida.id_concepte_pres.desc_concepte, "periodes": periodes, "total": total_periode})

                ######
                ########

        # tam_periodes = round(max_periodes/8) #lo dividimos entre 8 para el boostrap,ya que quedan col-md-8 como tamano maximo(hay 2 divs que ocupan 2,el concepto y el total)
        resultado.append({"dades_prj": projecte, "codi_resp": cod_responsable, "codi_prj": cod_projecte,
                          'centres_participants': centres_participants, 'participants_creaf': participants_creaf,
                          'participants_externs': participants_externs, 'financadors': financadors,
                          'receptors': receptors, 'canoniva': canoniva, 'despeses': despeses,
                          'total_concedit': despesa_total_concedit, 'total_iva': despesa_total_iva,
                          'total_canon': despesa_total_canon, 'total_net': despesa_total_net, 'partides': partides,
                          'totals_pres': totals, 'max_periodes': range(max_periodes),
                          'total_import_pres': total_import})


    context = {'llista_dades': resultado, 'titulo': "FITXA DADES"}
    return render(request, 'gestprj/cont_dades.html', context)

# ESTAT PRESUPOSTARI

@login_required(login_url='/menu/')
def cont_estat_pres(request):
    try:
        projectes = request.POST
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        resultado=[]
        for projecte_chk in projectes.getlist("prj_select"): # dentro de projectes tenemos prj_select que es una lista llena de xx-xxx.Aqui los obtenemos
            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte', 'percen_iva', 'percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte=projecte[0]# Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = concedit + importe['import_concedit']
            iva = concedit - (concedit / (1 + projecte['percen_iva'] / 100))
            canon = (concedit * projecte['percen_canon_creaf']) / (100 * (1 + projecte['percen_iva'] / 100))
            net_disponible = concedit - iva - canon

            concedit = round(concedit, 2)
            iva = round(iva, 2)
            canon = round(canon, 2)
            net_disponible = round(net_disponible, 2)
            #####
            num_periodes=1 #marcamos uno ya que pueden haber gastos totales sin periodos
            periodes=[]
            if PeriodicitatPres.objects.filter(id_projecte=projecte['id_projecte']):#Si hay periodos(el __lte es menor que o igual)
                #OJO!!! poner ", data_inicial__mte=fecha_min, data_final__lte=fecha_max"?
                for periode in PeriodicitatPres.objects.filter(id_projecte=projecte['id_projecte']).values('data_inicial','data_final','id_periodicitat'):
                    data_min_periode = datetime.strptime(str(periode['data_inicial']), "%Y-%m-%d")
                    data_max_periode = datetime.strptime(str(periode['data_final']), "%Y-%m-%d")
                    id_periodicitat = periode['id_periodicitat']
                    periodes.append({"id_periode":id_periodicitat,"num_periode":num_periodes,"data_min":str(data_min_periode),"data_max":str(data_max_periode)})
                    num_periodes += 1


            projecte["codi_resp"]=cod_responsable
            projecte["codi_prj"]=cod_projecte
            projecte["iva"]=iva
            projecte["canon"]=canon
            projecte["net_disponible"]=net_disponible
            projecte["concedit"]=concedit
            projecte["periodes"]=periodes
            projecte["data_min"]=str(fecha_min)
            projecte["data_max"]=str(fecha_max)


            resultado.append(projecte)

        context = { 'projectes':resultado,'titulo': "ESTAT PRESUPOSTARI"} # 'llista_estat_pres': llista_estat_pres,
    except:
        context = {'projectes': [], 'titulo': "ESTAT PRESUPOSTARI"}  # 'llista_estat_pres': llista_estat_pres,
    return render(request, 'gestprj/cont_estat_pres.html', context)



@login_required(login_url='/menu/') # AJAX 1 (SE RELLENAN LAS TABLAS)
def ListEstatPresDatos(request,datos):
    resultado=contabilitat_ajax.AjaxListEstatPresDatos(request,datos)
    return HttpResponse(resultado, content_type='application/json;')




def ListDespesesCompte(request,id_partida,cod,data_min,data_max): # AJAX 2 (SE MUESTRAN LOS DATOS
    resultado = contabilitat_ajax.AjaxListDespesesCompte(request,id_partida,cod,data_min,data_max)
    return HttpResponse(resultado, content_type='application/json;')


# DESPESES PROJECTE

@login_required(login_url='/menu/')
def cont_despeses(request):

    try:
        projectes = request.POST
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        resultado=[]
        for projecte_chk in projectes.getlist("prj_select"): # dentro de projectes tenemos prj_select que es una lista llena de xx-xxx.Aqui los obtenemos
            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte', 'percen_iva', 'percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte=projecte[0]# Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = concedit + importe['import_concedit']
            iva = concedit - (concedit / (1 + projecte['percen_iva'] / 100))
            canon = (concedit * projecte['percen_canon_creaf']) / (100 * (1 + projecte['percen_iva'] / 100))
            net_disponible = concedit - iva - canon

            concedit = round(concedit, 2)
            iva = round(iva, 2)
            canon = round(canon, 2)
            net_disponible = round(net_disponible, 2)
            #####
            num_periodes=1 #marcamos uno ya que pueden haber gastos totales sin periodos
            periodes=[]
            if PeriodicitatPres.objects.filter(id_projecte=projecte['id_projecte']):#Si hay periodos(el __lte es menor que o igual)
                #OJO!!! poner ", data_inicial__mte=fecha_min, data_final__lte=fecha_max"?
                for periode in PeriodicitatPres.objects.filter(id_projecte=projecte['id_projecte']).values('data_inicial','data_final','id_periodicitat'):
                    data_min_periode = datetime.strptime(str(periode['data_inicial']), "%Y-%m-%d")
                    data_max_periode = datetime.strptime(str(periode['data_final']), "%Y-%m-%d")
                    id_periodicitat = periode['id_periodicitat']
                    periodes.append({"id_periode":id_periodicitat,"num_periode":num_periodes,"data_min":str(data_min_periode),"data_max":str(data_max_periode)})
                    num_periodes += 1


            projecte["codi_resp"]=cod_responsable
            projecte["codi_prj"]=cod_projecte
            projecte["iva"]=iva
            projecte["canon"]=canon
            projecte["net_disponible"]=net_disponible
            projecte["concedit"]=concedit
            projecte["periodes"]=periodes
            projecte["data_min"]=str(fecha_min)
            projecte["data_max"]=str(fecha_max)


            resultado.append(projecte)

        context = { 'projectes':resultado,'fecha_min':str(fecha_min),'fecha_max':str(fecha_max),'titulo': "LLISTA DE DESPESES"} # 'llista_estat_pres': llista_estat_pres,
    except:
        context = {'projectes': [], 'titulo': "LLISTA DE DESPESES"}  # 'llista_estat_pres': llista_estat_pres,


    return render(request, 'gestprj/cont_despeses.html', context)

@login_required(login_url='/menu/')
def ListDespesesDatos(request,fecha_min,fecha_max,codigo): # AJAX1(SE RELLENAN LAS TABLAS)
    resultado=contabilitat_ajax.AjaxListDespesesDatos(request,fecha_min,fecha_max,codigo)
    return HttpResponse(resultado, content_type='application/json;')

# INGRESOS PROJECTE

@login_required(login_url='/menu/')
def cont_ingresos(request):
    try:
        projectes = request.POST
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):  # dentro de projectes tenemos prj_select que es una lista llena de xx-xxx.Aqui los obtenemos
            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte','percen_iva','percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte = projecte[0]  # Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = concedit + importe['import_concedit']
            iva = concedit - (concedit / (1 + projecte['percen_iva'] / 100))
            # canon = (concedit * projecte['percen_canon_creaf']) / (100 * (1 + projecte['percen_iva'] / 100))
            net_disponible = concedit - iva # OJO que este no usa el CANON

            concedit = round(concedit, 2)
            iva = round(iva, 2)
            # canon = round(canon, 2)
            net_disponible = round(net_disponible, 2)
            #####
            num_periodes = 1  # marcamos uno ya que pueden haber gastos totales sin periodos
            periodes = []
            if PeriodicitatPres.objects.filter(id_projecte=projecte['id_projecte']):  # Si hay periodos(el __lte es menor que o igual)
                # OJO!!! poner ", data_inicial__mte=fecha_min, data_final__lte=fecha_max"?
                for periode in PeriodicitatPres.objects.filter(id_projecte=projecte['id_projecte']).values('data_inicial', 'data_final', 'id_periodicitat'):
                    data_min_periode = datetime.strptime(str(periode['data_inicial']), "%Y-%m-%d")
                    data_max_periode = datetime.strptime(str(periode['data_final']), "%Y-%m-%d")
                    id_periodicitat = periode['id_periodicitat']
                    periodes.append({"id_periode": id_periodicitat, "num_periode": num_periodes, "data_min": str(data_min_periode),"data_max": str(data_max_periode)})
                    num_periodes += 1

            projecte["codi_resp"] = cod_responsable
            projecte["codi_prj"] = cod_projecte
            projecte["iva"] = iva
            # projecte["canon"] = canon
            projecte["net_disponible"] = net_disponible
            projecte["concedit"] = concedit
            projecte["periodes"] = periodes
            projecte["data_min"] = str(fecha_min)
            projecte["data_max"] = str(fecha_max)

            resultado.append(projecte)

        context = {'projectes': resultado, 'fecha_min': str(fecha_min), 'fecha_max': str(fecha_max),'titulo': "LLISTA DE INGRESOS"}  # 'llista_estat_pres': llista_estat_pres,
    except:
        context = {'projectes': [], 'titulo': "LLISTA DE INGRESOS"}  # 'llista_estat_pres': llista_estat_pres,

    return render(request, 'gestprj/cont_ingresos.html', context)


@login_required(login_url='/menu/')
def ListIngresosDatos(request,fecha_min,fecha_max,codigo): # AJAX1(SE RELLENAN LAS TABLAS)
    resultado = contabilitat_ajax.AjaxListIngresosDatos(request,fecha_min,fecha_max,codigo)
    return HttpResponse(resultado, content_type='application/json;')

@login_required(login_url='/menu/')
def cont_resum_estat_prj(request): # Ojo este es el unico que no usa AJAX ya que solo tiene una tabla

    # Ojo que este hace un return de 2 arrays,uno con los datos(llsita_dades[0]) y otro con los totales(llista_dades[1])
    projectes = request.POST

    ## En este caso devolveremos 2 arrays,uno con los datos y otro con los totales (mirar el return para mas info)
    fecha_min = datetime.strptime(projectes["data_min"], "%d-%m-%Y")
    fecha_max = datetime.strptime(projectes["data_max"], "%d-%m-%Y")
    cursor = connections['contabilitat'].cursor()
    resultado = []
    investigadores = {}  # diccionario
    proyectos = []
    nuevo_inv = 0  # es un chivato para indicar cuando empezamos a sumar los proyectos de otro investigador
    num_investigadores = 0


    # Averiguar el numero de investigadores a partir de inspeccionar todos los proyectos que hemos recibido
    for projecte_chk in projectes.getlist("prj_select"):
        cod_responsable = projecte_chk.split("-")[0]
        if int(cod_responsable) not in investigadores:
            investigadores[int(cod_responsable)] = int(cod_responsable)
            num_investigadores = num_investigadores + 1

    # Ahora empieza lo bueno
    for inv in investigadores:
        nuevo_inv = 1
        iva = 0
        canon_max = 0
        for projecte_chk in projectes.getlist("prj_select"):
            cod_responsable = projecte_chk.split("-")[0]

            if (inv == int(cod_responsable)):
                ##### Para extraer el objeto proyecto y el codigo:
                id_resp = Responsables.objects.get(
                    codi_resp=cod_responsable).id_resp  # OJO! el cod_resp 12 equivale al pinol pero tambien al usuaro del abel de prueva
                cod_projecte = projecte_chk.split("-")[1]
                projecte = Projectes.objects.get(codi_prj=cod_projecte,
                                                 id_resp=id_resp)  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
                ##### poner 0 en los codigos si son demasiado cortos para tener x tamano

                if len(cod_responsable) < 2:
                    cod_responsable = "0" + str(cod_responsable)
                if len(cod_projecte) < 3:
                    if len(cod_projecte) < 2:
                        cod_projecte = "00" + str(cod_projecte)
                    else:
                        cod_projecte = "0" + str(cod_projecte)
                #####
                codigo_entero = cod_responsable + cod_projecte
                #####

                ##### Cuentas:
                concedit = 0
                for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                    concedit = concedit + importe.import_concedit

                iva = concedit - (concedit / (1 + projecte.percen_iva / 100))
                canon = (concedit * projecte.percen_canon_creaf) / (100 * (1 + projecte.percen_iva / 100))
                net_disponible = concedit - iva - canon

                # Calculamos el canon mas grande entre el del creaf y el oficial,para luego calcular el canon total

                if concedit == 0:  # para evitar problemas con la division si es 0
                    percen_canon_oficial = 0.00
                else:
                    percen_canon_oficial = (
                    (projecte.canon_oficial / concedit) * (100 * (1 + projecte.percen_iva / 100)))

                if percen_canon_oficial > projecte.percen_canon_creaf:
                    canon_max = percen_canon_oficial
                else:
                    canon_max = projecte.percen_canon_creaf

                canon_total = round((concedit - iva) * (canon_max / 100))
                concedit = round(concedit, 2)
                iva = round(iva, 2)
                canon = round(canon, 2)
                net_disponible = round(net_disponible, 2)

                #############
                ### consulta SQL
                cursor.execute("SELECT ingressosD, ingressosH, despesesD, despesesH, canonD, canonH FROM "
                               "(SELECT CONVERT(varchar,Sum(DEBE))AS ingressosD, CONVERT(varchar,Sum(HABER))AS ingressosH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND CUENTAS.CUENTA LIKE '7%' AND CUENTAS.CUENTA NOT LIKE '79%' AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?))) AS ingressos,"
                               "(SELECT CONVERT(varchar,Sum(DEBE))AS despesesD, CONVERT(varchar,Sum(HABER))AS despesesH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '6%' OR CUENTAS.CUENTA LIKE '2%') AND CUENTAS.CUENTA NOT LIKE '6296'+(?) AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?))) AS despeses,"
                               "(SELECT CONVERT(varchar,Sum(DEBE))AS canonD, CONVERT(varchar,Sum(HABER))AS canonH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '7900%' OR CUENTAS.CUENTA LIKE '6296%') AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?))) AS canon",[codigo_entero, fecha_max, codigo_entero, codigo_entero, fecha_max, codigo_entero,fecha_max])

                projectfetch = dictfetchall(cursor)  # un cursor.description tambien sirve

                if projectfetch[0]["ingressosD"] is None:
                    projectfetch[0]["ingressosD"] = 0
                if projectfetch[0]["ingressosH"] is None:
                    projectfetch[0]["ingressosH"] = 0
                if projectfetch[0]["despesesD"] is None:
                    projectfetch[0]["despesesD"] = 0
                if projectfetch[0]["despesesH"] is None:
                    projectfetch[0]["despesesH"] = 0
                if projectfetch[0]["canonD"] is None:
                    projectfetch[0]["canonD"] = 0
                if projectfetch[0]["canonH"] is None:
                    projectfetch[0]["canonH"] = 0

                ingressosD = float(projectfetch[0]["ingressosD"])
                ingressosH = float(projectfetch[0]["ingressosH"])
                despesesD = float(projectfetch[0]["despesesD"])
                despesesH = float(projectfetch[0]["despesesH"])
                canonD = float(projectfetch[0]["canonD"])
                canonH = float(projectfetch[0]["canonH"])

                # Calculamos algunos campos a partir de lo obtenido de contabilidad
                ingressos = round(ingressosH - ingressosD, 2)
                despeses = round(despesesD - despesesH,
                                 2)  # OJO! que los que en los que estan tancats las despesas suelen coincir con el net_disponible,pero siempre es despesesD-H
                canon_aplicat = round(canonD - canonH, 2)
                disponible_caixa = round(ingressos - despeses - canon_aplicat, 2)
                disponible_real = round(concedit - iva - canon_total - despeses,
                                        2)  # OJO esta ok,solo que como algunos importes salen x100 tiene un valor elevado.
                pendent = round(abs(concedit - iva - ingressos), 2)
                #


                if nuevo_inv == 1:
                    nuevo_inv = 0
                    proyectos.append(projectfetch)
                    proyectos[0][0]["concedit"] = concedit
                    proyectos[0][0]["iva"] = iva
                    proyectos[0][0]["canon_total"] = canon_total
                    proyectos[0][0]["ingressos"] = ingressos
                    proyectos[0][0]["pendent"] = pendent
                    proyectos[0][0]["despeses"] = despeses
                    proyectos[0][0]["canon_aplicat"] = canon_aplicat
                    proyectos[0][0]["disponible_caixa"] = disponible_caixa
                    proyectos[0][0]["disponible_real"] = disponible_real



                else:

                    proyectos[0][0]["concedit"] = proyectos[0][0]["concedit"] + concedit
                    proyectos[0][0]["iva"] = proyectos[0][0]["iva"] + iva
                    proyectos[0][0]["canon_total"] = proyectos[0][0]["canon_total"] + canon_total
                    proyectos[0][0]["ingressos"] = proyectos[0][0]["ingressos"] + ingressos
                    proyectos[0][0]["pendent"] = proyectos[0][0]["pendent"] + pendent
                    proyectos[0][0]["despeses"] = proyectos[0][0]["despeses"] + despeses
                    proyectos[0][0]["canon_aplicat"] = proyectos[0][0]["canon_aplicat"] + canon_aplicat
                    proyectos[0][0]["disponible_caixa"] = proyectos[0][0]["disponible_caixa"] + disponible_caixa
                    proyectos[0][0]["disponible_real"] = proyectos[0][0]["disponible_real"] + disponible_real

                proyectos[0][0][
                    "cod_responsable"] = cod_responsable  # este y el de abajo so correctos pero se superponen una y otra vez por cada proyecto,a ver si se puede mejorar
                proyectos[0][0]["nom_responsable"] = Responsables.objects.get(
                    codi_resp=cod_responsable).id_usuari.nom_usuari

        resultado.append(proyectos)

        proyectos = []

    llista_dades = resultado

    context = {'llista_dades': llista_dades,'data_max':projectes["data_max"],'titulo': "RESUM ESTAT PROJECTES"}
    return render(request, 'gestprj/cont_resum_estat_prj.html', context)

@login_required(login_url='/menu/')
def cont_estat_prj_resp(request):

    try:
        projectes = request.POST
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        resultado=[]
        investigadores = {}  # diccionario
        # Averiguar el numero de investigadores a partir de inspeccionar todos los proyectos que hemos recibido
        for projecte_chk in projectes.getlist("prj_select"):
            cod_responsable = projecte_chk.split("-")[0]
            if int(cod_responsable) not in investigadores:
                investigadores[int(cod_responsable)]=int(cod_responsable)
                # num_investigadores=num_investigadores+1

        for inv in investigadores:
            nom_resp = Responsables.objects.get(codi_resp=inv).id_usuari.nom_usuari
            proyectos = ""
            for projecte_chk in projectes.getlist("prj_select"):
                cod_responsable = projecte_chk.split("-")[0]
                if(inv==int(cod_responsable)):
                    if proyectos == "":
                        proyectos = str(projecte_chk)
                    else:
                        proyectos = proyectos + "," + str(projecte_chk)

            resultado.append({"nom_responsable":nom_resp,"projectes":proyectos})

        context = {'responsables':resultado,"data_max":str(fecha_max),"data_min":str(fecha_min),'titulo': "ESTAT PROJECTES PER RESPONSABLE"} # 'llista_estat_pres': llista_estat_pres,
    except:
        context = {'responsables': [],"data_max":str(fecha_max),"data_min":str(fecha_min), 'titulo': "ESTAT PROJECTES PER RESPONSABLE"}  # 'llista_estat_pres': llista_estat_pres,
    return render(request, 'gestprj/cont_RESUM_estat_prj_resp.html', context)

@login_required(login_url='/menu/')
def ListEstatPrjRespDatos(request,fecha_min,fecha_max,proyectos): # AJAX1(SE RELLENAN LAS TABLAS)
    resultado= contabilitat_ajax.AjaxListEstatPrjRespDatos(request,fecha_min,fecha_max,proyectos)
    return HttpResponse(resultado, content_type='application/json;')

@login_required(login_url='/menu/')
def cont_resum_fitxa_major_prj(request): #RESUM PER PARTIDES

    try:
        projectes = request.POST
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        resultado=[]
        for projecte_chk in projectes.getlist("prj_select"): # dentro de projectes tenemos prj_select que es una lista llena de xx-xxx.Aqui los obtenemos
            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte', 'percen_iva', 'percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte=projecte[0]# Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = concedit + importe['import_concedit']
            iva = concedit - (concedit / (1 + projecte['percen_iva'] / 100))
            canon = (concedit * projecte['percen_canon_creaf']) / (100 * (1 + projecte['percen_iva'] / 100))
            net_disponible = concedit - iva - canon

            concedit = round(concedit, 2)
            iva = round(iva, 2)
            canon = round(canon, 2)
            net_disponible = round(net_disponible, 2)
            #####

            projecte["codi_resp"]=cod_responsable
            projecte["codi_prj"]=cod_projecte
            projecte["codigo_entero"] = projecte_chk
            projecte["iva"]=iva
            projecte["canon"]=canon
            projecte["net_disponible"]=net_disponible
            projecte["concedit"]=concedit
            projecte["data_min"]=str(fecha_min)
            projecte["data_max"]=str(fecha_max)

            resultado.append(projecte)

        context = { 'projectes':resultado,'titulo': "RESUM PER PARTIDES"}
    except:
        context = {'projectes': [], 'titulo': "RESUM PER PARTIDES"}
    return render(request, 'gestprj/cont_resum_fitxa_major_prj.html', context)


@login_required(login_url='/menu/')
def ListResumFitxaMajorPrjDatos(request,fecha_min,fecha_max,codigo): #AJAX1(SE RELLENAN LAS TABLAS)
    resultado = contabilitat_ajax.AjaxListResumFitxaMajorPrjDatos(request,fecha_min,fecha_max,codigo)
    return HttpResponse(resultado, content_type='application/json;')

def ListMovimentsCompte(request,compte,data_min,data_max): # AJAX 2
    resultado=contabilitat_ajax.AjaxListMovimentsCompte(request,compte,data_min,data_max)
    return HttpResponse(resultado, content_type='application/json')


@login_required(login_url='/menu/')
def cont_fitxa_major_prj(request): # INGRESSOS I DESPESES (FITXA MAJOR PRJ)

    try:
        projectes = request.POST
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        resultado=[]
        for projecte_chk in projectes.getlist("prj_select"): # dentro de projectes tenemos prj_select que es una lista llena de xx-xxx.Aqui los obtenemos
            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte', 'percen_iva', 'percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte=projecte[0]# Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = concedit + importe['import_concedit']
            iva = concedit - (concedit / (1 + projecte['percen_iva'] / 100))
            canon = (concedit * projecte['percen_canon_creaf']) / (100 * (1 + projecte['percen_iva'] / 100))
            net_disponible = concedit - iva - canon

            concedit = round(concedit, 2)
            iva = round(iva, 2)
            canon = round(canon, 2)
            net_disponible = round(net_disponible, 2)
            #####

            projecte["codi_resp"]=cod_responsable
            projecte["codi_prj"]=cod_projecte
            projecte["codigo_entero"] = projecte_chk
            projecte["iva"]=iva
            projecte["canon"]=canon
            projecte["net_disponible"]=net_disponible
            projecte["concedit"]=concedit
            projecte["data_min"]=str(fecha_min)
            projecte["data_max"]=str(fecha_max)

            resultado.append(projecte)

        context = { 'projectes':resultado,'titulo': "INGRESSOS I DESPESES"}
    except:
        context = {'projectes': [], 'titulo': "INGRESSOS I DESPESES"}
    return render(request, 'gestprj/cont_fitxa_major_prj.html', context)


@login_required(login_url='/menu/')
def ListFitxaMajorPrjDatos(request,fecha_min,fecha_max,codigo): # AJAX1(SE RELLENAN LAS TABLAS)
    resultado=contabilitat_ajax.AjaxListFitxaMajorPrjDatos(request,fecha_min,fecha_max,codigo)
    return HttpResponse(resultado, content_type='application/json;')

@login_required(login_url='/menu/')
def cont_resum_estat_canon(request):
    try:
        projectes = request.POST
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        resultado = []
        investigadores = {}  # diccionario
        # Averiguar el numero de investigadores a partir de inspeccionar todos los proyectos que hemos recibido
        for projecte_chk in projectes.getlist("prj_select"):
            cod_responsable = projecte_chk.split("-")[0]
            if int(cod_responsable) not in investigadores:
                investigadores[int(cod_responsable)] = int(cod_responsable)
                # num_investigadores=num_investigadores+1

        for inv in investigadores:
            nom_resp = Responsables.objects.get(codi_resp=inv).id_usuari.nom_usuari
            proyectos = ""
            for projecte_chk in projectes.getlist("prj_select"):
                cod_responsable = projecte_chk.split("-")[0]
                if (inv == int(cod_responsable)):
                    if proyectos == "":
                        proyectos = str(projecte_chk)
                    else:
                        proyectos = proyectos + "," + str(projecte_chk)

            resultado.append({"nom_responsable": nom_resp, "projectos": proyectos})

        context = {'responsables': resultado,"fecha_max": str(fecha_max), "fecha_min": str(fecha_min),'titulo': "RESUM ESTAT CANON PER RESPONSABLE"}  # 'llista_estat_pres': llista_estat_pres,
    except:
        context = {'responsables': [],"fecha_max": str(fecha_max), "fecha_min": str(fecha_min),'titulo': "RESUM ESTAT CANON PER RESPONSABLE"}  # 'llista_estat_pres': llista_estat_pres,

    return render(request, 'gestprj/cont_resum_estat_canon.html', context)

@login_required(login_url='/menu/')
def ListResumEstatCanonDatos(request,fecha_min,fecha_max,codigo): #AJAX1(SE RELLENAN LAS TABLAS)
    resultado = contabilitat_ajax.AjaxListResumEstatCanonDatos(request,fecha_min,fecha_max,codigo)
    return HttpResponse(resultado, content_type='application/json;')

@login_required(login_url='/menu/')
def cont_comptes_no_assignats(request):

    projectes = request.POST
    fecha_min = datetime.strptime(projectes["data_min"], "%d-%m-%Y")
    fecha_max = datetime.strptime(projectes["data_max"], "%d-%m-%Y")
    cursor = connections['contabilitat'].cursor()
    comptes = []
    resultado = []
    lista_codigos = ""
    saldo = 0
    total_carrec = 0
    total_ingressos = 0
    total_saldo = 0

    for projecte_chk in projectes.getlist("prj_select"):

        ##### Para extraer el objeto proyecto y el codigo:
        cod_responsable = projecte_chk.split("-")[0]
        id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
        cod_projecte = projecte_chk.split("-")[1]
        projecte = Projectes.objects.get(codi_prj=cod_projecte, id_resp=id_resp)
        ##### poner 0 en los codigos si son demasiado cortos para tener x tamano
        if len(cod_responsable) < 2:
            cod_responsable = "0" + str(cod_responsable)
        if len(cod_projecte) < 3:
            if len(cod_projecte) < 2:
                cod_projecte = "00" + str(cod_projecte)
            else:
                cod_projecte = "0" + str(cod_projecte)

        codigo_entero = cod_responsable + cod_projecte
        lista_codigos = lista_codigos + codigo_entero

    # 105 en el convert equivale al dd-mm-yyyy
    cursor.execute("SELECT CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(varchar(200),CUENTAS.DESCCUE) AS Titulo, CONVERT(varchar,Sum(DEBE))AS TotalDebe, CONVERT(varchar,Sum(HABER))AS TotalHaber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE ( (CUENTAS.CUENTA LIKE '2%' OR CUENTAS.CUENTA LIKE '6%' OR CUENTAS.CUENTA LIKE '7%') AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) AND (RIGHT(CUENTAS.CUENTA,5) NOT IN ((?))) ) GROUP BY CUENTAS.CUENTA,CUENTAS.DESCCUE ORDER BY CUENTAS.CUENTA",[fecha_max, fecha_min, lista_codigos])

    projectfetch = dictfetchall(cursor)  # un cursor.description tambien sirve

    ##### Para ir restando el saldo pendiente a medida que salen ingresos:
    for prjfet in projectfetch:
        if prjfet["TotalHaber"] == None:
            prjfet["TotalHaber"] = 0
        if prjfet["TotalDebe"] == None:
            prjfet["TotalDebe"] = 0

        saldo = round((saldo - float(prjfet["TotalDebe"])) + float(prjfet["TotalHaber"]), 2)
        prjfet["Saldo"] = saldo
        total_saldo = saldo
        total_carrec = total_carrec + float(prjfet["TotalHaber"])
        total_ingressos = total_ingressos + float(prjfet["TotalDebe"])

    resultado.append({"comptes": projectfetch, 'data_min': projectes["data_min"], 'data_max': projectes["data_max"],
                      "total_carrec": total_carrec, "total_ingressos": total_ingressos, "total_saldo": total_saldo})


    llista_dades = resultado

    context = {'llista_dades': llista_dades, 'titulo': "COMPTES NO ASSIGNATS A CAP PROJECTE"}
    return render(request, 'gestprj/cont_comptes_no_assignats.html', context)

@login_required(login_url='/menu/')
def ListJustificacionsCabecera(request,fecha_min,fecha_max): # AJAX PARA LAS JUSTIFICACIONES DE LA CABECERA
    resultado=contabilitat_ajax.AjaxListJustificacionsCabecera(request,fecha_min,fecha_max)
    return HttpResponse(resultado, content_type='application/json;')