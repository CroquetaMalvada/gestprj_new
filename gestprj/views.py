from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connections
from django.core import serializers
from gestprj.models import * #Projectes, TCategoriaPrj, TOrganismes, CentresParticipants, PersonalExtern, TUsuarisExterns, PersonalCreaf, TUsuarisCreaf, JustificPersonal, TFeines, Financadors, Receptors, JustificInternes, Renovacions, TConceptesPress, Pressupost, PeriodicitatPres, PeriodicitatPartida, Desglossaments, ClausDiferenCompte, JustificProjecte, AuditoriesProjecte, Responsables, PrjUsuaris
from django.db.models import Q
#from gestprj.forms import UsuariXarxaForm
from gestprj.forms import ProjectesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django_auth_ldap.config import LDAPGroupType
from gestprj.utils import usuari_a_responsable,id_resp_a_codi_responsable
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from gestprj.serializers import *
# GestCentresParticipantsSerializer, ProjectesSerializer, \
#     GestTOrganismesSerializer, PersonalExtern_i_organitzacioSerializer, \
#     TUsuarisExternsSerializer, GestTUsuarisExternsSerializer, PersonalExternSerializer, PersonalCreafSerializer, \
#     GestTUsuarisCreafSerializer, GestJustificPersonalSerializer, \
#     GestOrganismesFinSerializer, GestOrganismesRecSerializer, GestJustifInternesSerializer, GestRenovacionsSerializer, \
#     GestConceptesPressSerializer, GestPressupostSerializer, GestPeriodicitatPresSerializer, \
#     GestPeriodicitatPartidaSerializer, GestDesglossamentSerializer, GestJustificacionsProjecteSerializer, \
#     GestAuditoriesSerializer, GestPrjUsuarisSerializer, ResponsablesSerializer, GestResponsablesSerializer
from gestprj import pk,contabilitat_ajax #,consultes_cont
from django.db import transaction
from datetime import datetime, timedelta
from calendar import monthrange
from decimal import *
import json

from openpyxl import  Workbook, load_workbook
from openpyxl.writer.excel import save_virtual_workbook #util para el httpresponse
import unicodecsv as csv # instalado con el pip ya que el csv a secas no incluye unicode

# #funcion para comprovar si el usuario es admin o investigador
# def not_in_student_group(user):
#     """Use with a ``user_passes_test`` decorator to restrict access to
#     authenticated users who are not in the "Student" group."""
#     return user.groups.filter(name='Admins gestprj').exists()


###
def es_admin(user):
    return user.groups.filter(name="Admins gestprj").exists()

def es_usuario_valido(user):
    if user.groups.filter(name="Admins gestprj").exists() or user.groups.filter(name="Mods gestprj").exists() or user.groups.filter(name="Investigadors Principals").exists():
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
@user_passes_test(es_admin,login_url='/comptabilitat/')
def list_projectes(request): # poner ajax para funciones_datatables,pero no es nada urgente
    # llista_projectes = TUsuarisXarxa.objects.all()
    # usuarixarxa = usuari_xarxa_a_user(request)
    if request.user.groups.filter(name="Admins gestprj").exists() or request.user.groups.filter(name="Mods gestprj").exists():#si el usuario es un admin,muetra todos los proyectos
        llista_projectes = Projectes.objects.select_related('id_estat_prj').all()
    else:#sino solo muestra SUS proyectos
        responsable = usuari_a_responsable(request)

        if responsable is not None:
            llista_projectes = Projectes.objects.filter(id_resp__id_resp=responsable.id_resp)
        else:
            llista_projectes = None

    for projecte in llista_projectes:
        ##### poner 0 en los codigos si son demasiado cortos para tener x tamano
        cod_projecte=str(projecte.codi_prj)
        cod_responsable=str(projecte.id_resp.codi_resp)
        if len(cod_responsable) < 2:
            cod_responsable = "0" + str(cod_responsable)
        if len(cod_projecte) < 3:
            if len(cod_projecte) < 2:
                cod_projecte = "00" + str(cod_projecte)
            else:
                cod_projecte = "0" + str(cod_projecte)

        codigo_entero = cod_responsable + cod_projecte
        projecte.codigo_entero=codigo_entero #creamos codigo_entero dentro el objeto
        ######
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
            if (user.groups.filter(name="Admins gestprj").exists() or user.groups.filter(name="Mods gestprj").exists() or user.groups.filter(name="Investigadors Principals").exists()):# y ademas forma parte de alguno de los grupos necesarios
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

# USUARIS CREAF ######################
def ListUsuarisCreafSelect(request):  # AJAX
    resultado = contabilitat_ajax.AjaxListUsuarisCreafSelect()
    return HttpResponse(resultado, content_type='application/json;')

# USUARIS XARXA ######################
def ListUsuarisXarxaSelect(request):  # AJAX
    resultado = contabilitat_ajax.AjaxListUsuarisXarxaSelect()
    return HttpResponse(resultado, content_type='application/json;')

# USUARIS EXTERNS ######################
def ListUsuarisExternsSelect(request):  # AJAX
    resultado = contabilitat_ajax.AjaxListUsuarisExternsSelect()
    return HttpResponse(resultado, content_type='application/json;')

# RESPONSABLES ######################
def ListResponsablesSelect(request):  # AJAX
    resultado = contabilitat_ajax.AjaxListResponsablesSelect()
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
class ListPersonalExternProjecte(generics.ListAPIView):  # muestra los usuarios externos que participan en un proyecto junto con su organizacion
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

# USUARIS XARXA #################
class ListUsuarisXarxa(generics.ListAPIView):  # todos los usuarios xarxa
    serializer_class = GestTUsuarisXarxaSerializer

    def get_queryset(self):
        return TUsuarisXarxa.objects.all().order_by('nom_xarxa')

class GestTUsuarisXarxa(viewsets.ModelViewSet):
    queryset = TUsuarisXarxa.objects.all()
    serializer_class = GestTUsuarisXarxaSerializer


# RESPOSNABLESS #################
class ListResponsables(generics.ListAPIView):  # todos los responsables(usamos serializer ya que no es el  select y necesitaremos la url del serializer)
    serializer_class = ResponsablesSerializer

    def get_queryset(self):
        return Responsables.objects.all().order_by('codi_resp')

class GestResponsables(viewsets.ModelViewSet):
    queryset = Responsables.objects.all()
    serializer_class = GestResponsablesSerializer


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
            #return Response(GestDesglossamentSerializer(Desglossaments.objects.all(), many=True).data)
            return Desglossaments.objects.all()
        else:
            _id_partida = self.kwargs['id_partida']
            #return Response(GestDesglossamentSerializer(Desglossaments.objects.filter(id_partida=_id_partida), many=True).data)
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

# COMPROMETIDO PERSONAL
class ListCompromesPersonal(generics.ListCreateAPIView):
    serializer_class = GestComprometidoPersonalSerializer

    def get_queryset(self):
        if self.kwargs['id_projecte'] is None:
            return CompromesPersonal.objects.all()
        else:
            _id_projecte = self.kwargs['id_projecte']
            return CompromesPersonal.objects.filter(id_projecte=_id_projecte)



class GestComprometidoPersonal(viewsets.ModelViewSet):
    queryset = CompromesPersonal.objects.all()
    serializer_class = GestComprometidoPersonalSerializer


# JSON DE COMPROMES
# def ListCompromes(request,id_projecte):
#     resultado=[]
#     id_prj=id_projecte
#     datos_prj=Projectes.objects.filter(id_projecte=id_prj).values("data_inici_prj","data_fi_prj","id_resp__codi_resp","codi_prj").first()
#     cursor = connections['contabilitat'].cursor()
#     partidas = []
#     # if PeriodicitatPres.objects.filter(id_projecte=id_prj):  # Si hay periodos(el __lte es menor que o igual)
#     #     # OJO!!! poner ", data_inicial__mte=fecha_min, data_final__lte=fecha_max"?
#     #     for periode in PeriodicitatPres.objects.filter(id_projecte=projecte['id_projecte']).values('data_inicial',
#     #                                                                                                'data_final',
#     #                                                                                                'id_periodicitat'):
#     #         data_min_periode = datetime.strptime(str(periode['data_inicial'].date()), "%Y-%m-%d")
#     #         data_max_periode = datetime.strptime(str(periode['data_final'].date()), "%Y-%m-%d")
#     #         id_periodicitat = periode['id_periodicitat']
#     #         periodes.append(
#     #             {"id_periode": id_periodicitat, "num_periode": num_periodes, "data_min": str(data_min_periode),
#     #              "data_max": str(data_max_periode)})
#     #         num_periodes += 1
#     for partida in Pressupost.objects.filter(id_projecte=id_prj).values('id_partida','id_concepte_pres__desc_concepte','import_field'):  # partidas de proyecto
#         id_partida = partida['id_partida']
#         desc_partida = partida['id_concepte_pres__desc_concepte']
#         pressupostat = float(partida['import_field'])
#         data_min =datos_prj["data_inici_prj"].date() # obtener solo la fecha sin horas ni nada de eso
#         data_max = datos_prj["data_fi_prj"].date() # .replace(tzinfo=None)
#         cod_responsable = str(datos_prj["id_resp__codi_resp"])
#         cod_projecte = str(datos_prj["codi_prj"])
#         ##### poner 0 en los codigos si son demasiado cortos para tener x tamano
#         if len(cod_responsable) < 2:
#             cod_responsable = "0" + str(cod_responsable)
#         if len(cod_projecte) < 3:
#             if len(cod_projecte) < 2:
#                 cod_projecte = "00" + str(cod_projecte)
#             else:
#                 cod_projecte = "0" + str(cod_projecte)
#         #####
#         codigo_entero = cod_responsable + cod_projecte
#         #####
#         # data_min = datetime.strptime(str(data_min), "%Y-%m-%d").date() #Ojo este es str F time
#         # data_max = datetime.strptime(str(data_max), "%Y-%m-%d").date()
#
#         ### para obtener el gastat
#         gastat = 0
#         comprometido= 0
#         for compte in Desglossaments.objects.filter(id_partida=id_partida).values('compte'):
#             cod_compte = str(compte['compte'])
#             if cod_compte is None:
#                 cod_compte = "0000"
#             # primer_digito=str(cod_compte)[0] # solo son cuentas contables los que empiezan por 6 y 2
#             # if primer_digito =='6' or primer_digito =='2' :
#             if len(cod_compte) < 4:
#                 if len(cod_compte) < 3:
#                     if len(cod_compte) < 2:
#                         cod_compte = cod_compte + "%%%"
#                     else:
#                         cod_compte = cod_compte + "%%"
#                 else:
#                     cod_compte = cod_compte + "%"
#
#             coste_mes=0
#             # Ojo parece que se necesitan 3 espacios en el codigo de centrocoste2,puede ser por la importacion que hicieron los de erp?los datos nuevos introducidos tambien tienen esos 3 espacios?
#             # OJO UTILIZAR FECHAS?
#             cursor.execute(
#                 "SELECT DEBE,HABER,DESCAPU FROM __ASIENTOS WHERE CENTROCOSTE2='   '+%s AND ( CONVERT(date,FECHA,121)<=%s AND CONVERT(date,FECHA,121)>=%s ) AND TIPAPU='N' AND IDCUENTA IN (SELECT IDCUENTA FROM CUENTAS WHERE CUENTA LIKE %s+'%' ) ",
#                 (codigo_entero, str(data_max), str(data_min), cod_compte))  # AND ( FECHA<'2017-01-01 00:00:00.000' )
#             cuentacont = dictfetchall(cursor)
#             if cuentacont:
#                 for cont in cuentacont:
#                     if cont["DEBE"] is None:
#                         cont["DEBE"] = 0
#                     if cont["HABER"] is None:
#                         cont["HABER"] = 0
#                     gastat = gastat + (Decimal(cont["DEBE"] - cont["HABER"]))
#                     coste_mes=(Decimal(cont["DEBE"] - cont["HABER"]))
#             ### Comprometido
#             # duracion_total=data_max-data_min
#
#             duracion_total=obtener_meses(data_min,data_max)
#             fecha_pendiente=duracion_total-(obtener_meses(data_min,datetime.now().date()))
#             comprometido=comprometido+(fecha_pendiente*coste_mes)
#             ###
#         libre=pressupostat-float(gastat-comprometido)
#         saldo = pressupostat - float(gastat)  # pasamos datos a float ya que los decimal no los pilla bien el json
#         partidas.append({"desc_partida": desc_partida, "pressupostat": float(pressupostat), "gastat": float(gastat),
#                          'compromes':float(comprometido),'lliure':libre,'id_partida': str(id_partida), 'codigo_entero': codigo_entero,
#                          'fecha_min': str(data_min), 'fecha_max': str(data_max)})
#     resultado = json.dumps(partidas)
#     return HttpResponse(resultado, content_type='application/json;')

# def ListCompromesPartida(request,id_partida,id_projecte): # el del dialog
#     if int(id_partida) != 0:
#         resultado=[]
#         # id_prj=id_projecte
#         datos_prj=Projectes.objects.filter(id_projecte=id_projecte).values("data_inici_prj","data_fi_prj","id_resp__codi_resp","codi_prj").first()
#         cursor = connections['contabilitat'].cursor()
#         # partidas = []
#
#         #for partida in Pressupost.objects.filter(id_partida=id_partida).values('id_partida','id_concepte_pres__desc_concepte','import_field'):  # partidas de proyecto
#         id_partida = id_partida
#         # desc_partida = partida['id_concepte_pres__desc_concepte']
#         pressupostat = float(getattr(Pressupost.objects.get(id_partida=id_partida),'import_field')) # float(partida['import_field'])
#         data_min =datos_prj["data_inici_prj"].date() # obtener solo la fecha sin horas ni nada de eso
#         data_max = datos_prj["data_fi_prj"].date() # .replace(tzinfo=None)
#         cod_responsable = str(datos_prj["id_resp__codi_resp"])
#         cod_projecte = str(datos_prj["codi_prj"])
#         ##### poner 0 en los codigos si son demasiado cortos para tener x tamano
#         if len(cod_responsable) < 2:
#             cod_responsable = "0" + str(cod_responsable)
#         if len(cod_projecte) < 3:
#             if len(cod_projecte) < 2:
#                 cod_projecte = "00" + str(cod_projecte)
#             else:
#                 cod_projecte = "0" + str(cod_projecte)
#         #####
#         codigo_entero = cod_responsable + cod_projecte
#         #####
#         # data_min = datetime.strptime(str(data_min), "%Y-%m-%d").date() #Ojo este es str F time
#         # data_max = datetime.strptime(str(data_max), "%Y-%m-%d").date()
#
#         ### para obtener el gastat
#         gastat = 0
#         comprometido= 0
#         for compte in Desglossaments.objects.filter(id_partida=id_partida).values('compte'):
#             cod_compte = str(compte['compte'])
#             if cod_compte is None:
#                 cod_compte = "0000"
#             # primer_digito=str(cod_compte)[0] # solo son cuentas contables los que empiezan por 6 y 2
#             # if primer_digito =='6' or primer_digito =='2' :
#             if len(cod_compte) < 4:
#                 if len(cod_compte) < 3:
#                     if len(cod_compte) < 2:
#                         cod_compte = cod_compte + "%%%"
#                     else:
#                         cod_compte = cod_compte + "%%"
#                 else:
#                     cod_compte = cod_compte + "%"
#
#             coste_mes=0
#             # Ojo parece que se necesitan 3 espacios en el codigo de centrocoste2,puede ser por la importacion que hicieron los de erp?los datos nuevos introducidos tambien tienen esos 3 espacios?
#             # OJO UTILIZAR FECHAS?
#             cursor.execute(
#                 "SELECT DEBE,HABER,DESCAPU FROM __ASIENTOS WHERE CENTROCOSTE2='   '+%s AND ( CONVERT(date,FECHA,121)<=%s AND CONVERT(date,FECHA,121)>=%s ) AND TIPAPU='N' AND IDCUENTA IN (SELECT IDCUENTA FROM CUENTAS WHERE CUENTA LIKE %s+'%' ) ",
#                 (codigo_entero, str(data_max), str(data_min), cod_compte))  # AND ( FECHA<'2017-01-01 00:00:00.000' )
#             cuentacont = dictfetchall(cursor)
#             if cuentacont:
#                 for cont in cuentacont:
#                     if cont["DEBE"] is None:
#                         cont["DEBE"] = 0
#                     if cont["HABER"] is None:
#                         cont["HABER"] = 0
#                     gastat = gastat + (Decimal(cont["DEBE"] - cont["HABER"]))
#                     coste_mes=(Decimal(cont["DEBE"] - cont["HABER"]))
#             ### Comprometido
#             # duracion_total=data_max-data_min
#
#             duracion_total=obtener_meses(data_min,data_max)
#             fecha_pendiente=duracion_total-(obtener_meses(data_min,datetime.now().date()))
#             comprometido=fecha_pendiente*coste_mes
#             ###
#             libre=pressupostat-float(gastat-comprometido)
#
#             resultado.append({"cuenta": str(compte['compte'])+codigo_entero, "coste_mes": float(coste_mes), "data_inici": str(data_min), "data_final": str(data_max),
#                              'duracio_total':duracion_total,'duracio_pendent':fecha_pendiente,'compromes': float(comprometido)})
#         resultado = json.dumps(resultado)
#         return HttpResponse(resultado, content_type='application/json;')
#     else:
#         return HttpResponse([{}], content_type='application/json;')



def obtener_meses(fecha1,fecha2): # obtener la diferencia en meses de 2 fechas
    #Ojo redondear hacia rriba si hay pocos dias de diferencia?
    delta = 0
    while True:
        mdays = monthrange(fecha1.year, fecha1.month)[1]
        fecha1 += timedelta(days=mdays)
        if fecha1 <= fecha2:
            delta += 1
        else:
            break
    return delta

# JSON DECOMPROMES DE COMPTE


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

def json_vacio_results(request):
    return HttpResponse(json.dumps({"results":""}), content_type='application/json;')

@login_required(login_url='/menu/')
def list_projectes_cont(request): #simplemente carga la template
    context = { 'titulo': "COMPTABILITAT"} # 'llista_projectes': llista_projectes ,
    return render(request, 'gestprj/comptabilitat.html', context)

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

#AJAX PARA VER COMPROMETIDO DE UN PROYECTO
def ListCompromesProjecte(request,id_projecte,codigo_entero):
    resultado=contabilitat_ajax.AjaxListCompromesProjecte(request,id_projecte,codigo_entero)
    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json')

#AJAX PARA VER COMPROMETIDO DE UNA CUENTA
def ListCompromesCompte(request,tipo_comp,id_projecte,codigo,compte):
    resultado=contabilitat_ajax.AjaxListCompromesCompte(request,tipo_comp,id_projecte,codigo,[compte])
    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json')

#AJAX PARA VER COMPROMETIDO DE VARIAS CUENTAS(COMO UNA PARTIDA) DE UN PROYECTO
def ListCompromesLlistaComptes(request,id_projecte,codigo_entero,llista_comptes):
    resultado=contabilitat_ajax.AjaxListCompromesLlistaComptes(request,id_projecte,codigo_entero,llista_comptes)
    return HttpResponse(resultado, content_type='application/json')

#AJAX PARA VER LAS LINEAS DE UN ALBARAN
def LineasAlbaran(request,id_albaran):
    resultado=contabilitat_ajax.AjaxLineasAlbaran(request,id_albaran)
    return HttpResponse(resultado, content_type='application/json')

#AJAX PARA VER LAS LINEAS DE UN PEDIDO
def LineasPedido(request,id_pedido):
    resultado=contabilitat_ajax.AjaxLineasPedido(request,id_pedido)
    return HttpResponse(resultado, content_type='application/json')

#AJAX PARA VER LAS LINEAS DE UN ALBARAN DETALLADAMENTE EN FACTURA
def LineasAlbaranDetalles(request,id_albaran):
    resultado=contabilitat_ajax.AjaxLineasAlbaranDetalles(request,id_albaran)
    return HttpResponse(resultado, content_type='application/json')

#AJAX PARA VER LAS LINEAS DE UN PEDIDO DETALLADAMENTE EN FACTURA ( PDF )
def LineasPedidoDetalles(request,num_apunte):
    resultado=contabilitat_ajax.AjaxLineasPedidoDetalles(request,num_apunte)
    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json')

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
        projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp)  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj

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

        percen_iva = round(0.0, 4)
        if projecte.percen_iva:
            percen_iva = round(float(projecte.percen_iva), 4)

        percen_canon_creaf = round(0.0, 4)
        if projecte.percen_canon_creaf:
            percen_canon_creaf = round(float(projecte.percen_canon_creaf), 4)

        canon_oficial = round(0.0, 4)
        if projecte.canon_oficial:
            canon_oficial = round(float(projecte.canon_oficial), 2)

        # calculados a mano
        if concedit == 0:  # para evitar problemas con la division si es 0
            percen_canon_oficial = 0.00
        else:
            percen_canon_oficial = round(((canon_oficial / concedit) * (100 * (1 + percen_iva / 100))), 4)
        canon_creaf = round(((concedit * float(percen_canon_creaf)) / (100 * (1 + percen_iva / 100))), 2)
        diferencia_per = round((percen_canon_oficial - percen_canon_creaf), 4)
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
            iva = round(((import_concedit * percen_iva) / (100 * (1 + percen_iva / 100))), 2)
            despesa_total_iva = despesa_total_iva + iva
            canon = round(((import_concedit * percen_canon_creaf) / (100 * (1 + percen_iva / 100))), 2)
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

# ESTAT PRESUPOSTARI  *DIVIDIDO EN 3 PARTES

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
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte', 'canon_oficial' ,'percen_iva', 'percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte=projecte[0]# Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = round(concedit + float(importe['import_concedit']),2)

            percen_iva = 0
            if projecte['percen_iva']:
                percen_iva = round(float(projecte['percen_iva']), 2)
            projecte['percen_iva'] = percen_iva

            percen_canon_creaf = 0
            if projecte['percen_canon_creaf']:
                percen_canon_creaf = round(projecte['percen_canon_creaf'], 2)
            projecte['percen_canon_creaf'] = percen_canon_creaf

            canon_oficial = 0
            if projecte['canon_oficial']:
                canon_oficial = round(projecte['canon_oficial'], 2)
            projecte['canon_oficial'] = canon_oficial

            iva = concedit - (concedit / (1 + percen_iva / 100))
            canon = (concedit * float(percen_canon_creaf)) / (100 * (1 + percen_iva / 100)) #Ojo Ahora con Python3 el round no siempre pasa a float
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
                    # data_min_periode = periode['data_inicial']
                    # data_max_periode = periode['data_final']
                    data_min_periode = datetime.strptime(str(periode['data_inicial'].date()), "%Y-%m-%d").strftime('%d-%m-%Y')
                    data_max_periode = datetime.strptime(str(periode['data_final'].date()), "%Y-%m-%d").strftime('%d-%m-%Y')
                    id_periodicitat = periode['id_periodicitat']
                    periodes.append({"id_periode":id_periodicitat,"num_periode":num_periodes,"data_min":str(data_min_periode),"data_max":str(data_max_periode)})
                    num_periodes += 1

            # Obtener el comprometido# Ojo parece que este no se usa ya que es solo para crear la tabla!
            compromes = 0
            try:
                for comp in CompromesPersonal.objects.filter(id_projecte=projecte.id_projecte).values("cost","data_inici","data_fi"):
                    fecha_actual = datetime.today().date()

                    coste = comp["cost"]
                    fecha_ini = comp["data_inici"]
                    fecha_fin = comp["data_fi"]
                    dif = fecha_fin - fecha_ini
                    duracion_total = dif.days
                    fecha_calculo = datetime.today().date()  # para calcular la fecha calculo obtenemos el ultimo dia del mes anterior
                    fecha_calculo = fecha_calculo.replace(day=1)
                    fecha_calculo = fecha_calculo - timedelta(days=1)
                    dif = fecha_fin - fecha_calculo
                    duracion_pendiente = dif.days
                    compromes = compromes + (duracion_pendiente * (coste / Decimal(30.42)))
            except:
                compromes = 0
            compromes = float(compromes)
            #


            projecte["codi_resp"]=cod_responsable
            projecte["codi_prj"]=cod_projecte
            projecte["iva"]=iva
            projecte["canon"]=canon
            projecte["net_disponible"]=net_disponible
            projecte["concedit"]=concedit
            projecte["periodes"]=periodes
            projecte["data_min"]=str(fecha_min)
            projecte["data_max"]=str(fecha_max)

            projecte["compromes"] = compromes


            resultado.append(projecte)

        context = { 'projectes':resultado,'titulo': "ESTAT PRESUPOSTARI"} # 'llista_estat_pres': llista_estat_pres,
    except:
        context = {'projectes': [], 'titulo': "ESTAT PRESUPOSTARI"}  # 'llista_estat_pres': llista_estat_pres,
    return render(request, 'gestprj/cont_estat_pres.html', context)



@login_required(login_url='/menu/') # AJAX 1 (SE RELLENAN LAS TABLAS)
def ListEstatPresDatos(request,datos):
    resultado=contabilitat_ajax.AjaxListEstatPresDatos(request,datos)
    return HttpResponse(resultado, content_type='application/json;')

def ListDespesesCompte(request,id_partida,cod,data_min,data_max): # AJAX 2 (SE MUESTRAN LOS DATOS AL CLICAR BOTON
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
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte', 'canon_oficial','percen_iva', 'percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte=projecte[0]# Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = round(concedit + float(importe['import_concedit']),2)

            percen_iva = 0
            if projecte['percen_iva']:
                percen_iva = round(float(projecte['percen_iva']), 2)
            projecte['percen_iva'] = percen_iva

            percen_canon_creaf = 0
            if projecte['percen_canon_creaf']:
                percen_canon_creaf = round(projecte['percen_canon_creaf'], 2)
            projecte['percen_canon_creaf'] = percen_canon_creaf

            canon_oficial = 0
            if projecte['canon_oficial']:
                canon_oficial = round(projecte['canon_oficial'], 2)
            projecte['canon_oficial'] = canon_oficial

            iva = concedit - (concedit / (1 + percen_iva / 100))
            canon = (concedit * float(percen_canon_creaf)) / (100 * (1 + percen_iva / 100))
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
                    data_min_periode = datetime.strptime(str(periode['data_inicial'].date()), "%Y-%m-%d")
                    data_max_periode = datetime.strptime(str(periode['data_final'].date()), "%Y-%m-%d")
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
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte','percen_iva', 'canon_oficial','percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte = projecte[0]  # Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = round(concedit + float(importe['import_concedit']),2)

            percen_iva = 0
            if projecte['percen_iva']:
                percen_iva = round(float(projecte['percen_iva']), 2)
            projecte['percen_iva'] = percen_iva

            percen_canon_creaf = 0
            if projecte['percen_canon_creaf']:
                percen_canon_creaf = round(projecte['percen_canon_creaf'], 2)
            projecte['percen_canon_creaf'] = percen_canon_creaf

            canon_oficial = 0
            if projecte['canon_oficial']:
                canon_oficial = round(projecte['canon_oficial'], 2)
            projecte['canon_oficial'] = canon_oficial

            iva = concedit - (concedit / (1 + percen_iva / 100))
            # canon = (concedit * float(percen_canon_creaf)) / (100 * (1 + percen_iva / 100))
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
                    data_min_periode = datetime.strptime(str(periode['data_inicial'].date()), "%Y-%m-%d")
                    data_max_periode = datetime.strptime(str(periode['data_final'].date()), "%Y-%m-%d")
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
                id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp  # OJO! el cod_resp 12 equivale al pinol pero tambien al usuaro del abel de prueva
                cod_projecte = projecte_chk.split("-")[1]
                projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp)  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
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

                # CANON I IVA
                concedit = 0
                for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                    concedit = round(concedit + float(importe.import_concedit), 2)
                # vienen en la tabla:
                # vienen en la tabla:

                percen_iva = round(0.0, 4)
                if projecte.percen_iva:
                    percen_iva = round(float(projecte.percen_iva), 4)

                percen_canon_creaf = round(0.0, 4)
                if projecte.percen_canon_creaf:
                    percen_canon_creaf = round(float(projecte.percen_canon_creaf), 4)

                canon_oficial = round(0.0, 4)
                if projecte.canon_oficial:
                    canon_oficial = round(float(projecte.canon_oficial), 2)

                # Calculamos el canon mas grande entre el del creaf y el oficial,para luego calcular el canon total

                if concedit == 0:  # para evitar problemas con la division si es 0
                    percen_canon_oficial = 0.00
                else:
                    percen_canon_oficial = (
                    (canon_oficial / concedit) * (100 * (1 + percen_iva / 100)))

                if percen_canon_oficial > projecte.percen_canon_creaf:
                    canon_max = percen_canon_oficial
                else:
                    canon_max = percen_canon_creaf

                iva = concedit - (concedit / (1 + percen_iva / 100))
                canon = (concedit * float(percen_canon_creaf)) / (100 * (1 + percen_iva / 100))
                net_disponible = concedit - iva - canon

                canon_total = round((concedit - iva) * (canon_max / 100))
                concedit = round(concedit, 2)
                iva = round(iva, 2)
                canon = round(canon, 2)
                net_disponible = round(net_disponible, 2)

                #############
                # Obtener el comprometido #
                compromes = 0
                try:
                    for comp in CompromesPersonal.objects.filter(id_projecte=projecte.id_projecte).values("cost", "data_inici", "data_fi"):
                        fecha_actual = datetime.today().date()

                        coste = comp["cost"]
                        fecha_ini = comp["data_inici"]
                        fecha_fin = comp["data_fi"]
                        dif = fecha_fin - fecha_ini
                        duracion_total = dif.days
                        fecha_calculo = datetime.today().date() #para calcular la fecha calculo obtenemos el ultimo dia del mes anterior
                        fecha_calculo = fecha_calculo.replace(day=1)
                        fecha_calculo = fecha_calculo - timedelta(days=1)
                        dif = fecha_fin - fecha_calculo
                        duracion_pendiente = dif.days
                        compromes = compromes + (duracion_pendiente * (coste / Decimal(30.42)))
                except:
                    compromes = 0
                compromes = float(compromes)
                #
                ### consulta SQL
                cursor.execute("SELECT ingressosD, ingressosH, despesesD, despesesH, canonD, canonH FROM "
                               "(SELECT CONVERT(varchar,Sum(DEBE))AS ingressosD, CONVERT(varchar,Sum(HABER))AS ingressosH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+%s AND CUENTAS.CUENTA LIKE '7%%' AND CUENTAS.CUENTA NOT LIKE '79%%' AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=%s)) AS ingressos,"
                               "(SELECT CONVERT(varchar,Sum(DEBE))AS despesesD, CONVERT(varchar,Sum(HABER))AS despesesH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+%s AND (CUENTAS.CUENTA LIKE '6%%' OR CUENTAS.CUENTA LIKE '2%%') AND CUENTAS.CUENTA NOT LIKE '6296%%' AND CUENTAS.CUENTA NOT LIKE '6901%%' AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=%s)) AS despeses,"
                               "(SELECT CONVERT(varchar,Sum(DEBE))AS canonD, CONVERT(varchar,Sum(HABER))AS canonH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+%s AND (CUENTAS.CUENTA LIKE '7900%%' OR CUENTAS.CUENTA LIKE '6296%%' OR CUENTAS.CUENTA LIKE '6901%%') AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=%s)) AS canon",(codigo_entero, fecha_max, codigo_entero, fecha_max, codigo_entero,fecha_max))

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
                disponible_real = round(concedit - iva - canon_total - despeses, 2)  # OJO esta ok,solo que como algunos importes salen x100 tiene un valor elevado.
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

                proyectos[0][0]["disponible_real"] = proyectos[0][0]["disponible_real"] -compromes
                proyectos[0][0]["cod_responsable"] = cod_responsable  # este y el de abajo so correctos pero se superponen una y otra vez por cada proyecto,a ver si se puede mejorar
                proyectos[0][0]["nom_responsable"] = Responsables.objects.get(codi_resp=cod_responsable).id_usuari.nom_usuari
                proyectos[0][0]["compromes"] = compromes

        resultado.append(proyectos)

        proyectos = []

    llista_dades = resultado

    # Cerramos el cursor
    cursor.close()

    context = {'llista_dades': llista_dades,'data_max':projectes["data_max"],'titulo': "RESUM ESTAT PROJECTES"}
    return render(request, 'gestprj/cont_resum_estat_prj.html', context)

# ESTAT PROJECTE PER RESPONSABLE ###########

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

def imprimir_resum_estat_prj_resp(request): # IMPRIMIR LISTADO DE ESOS PROYECTOS
    try:
        projectes = request.POST["impr_prjs"].split(",")
        projectes.remove("")
        fecha_min = request.POST["impr_data_min"]
        fecha_max = request.POST["impr_data_max"]
        resultado=[]
        investigadores = {}  # diccionario
        # Averiguar el numero de investigadores a partir de inspeccionar todos los proyectos que hemos recibido
        for projecte_chk in projectes:
            cod_responsable = projecte_chk.split("-")[0]
            if int(cod_responsable) not in investigadores:
                investigadores[int(cod_responsable)]=int(cod_responsable)
                # num_investigadores=num_investigadores+1

        for inv in investigadores:
            nom_resp = Responsables.objects.get(codi_resp=inv).id_usuari.nom_usuari
            proyectos = ""
            totales = []
            for projecte_chk in projectes:
                cod_responsable = projecte_chk.split("-")[0]
                if(inv==int(cod_responsable)):
                    if proyectos == "":
                        proyectos = str(projecte_chk)
                    else:
                        proyectos = proyectos + "," + str(projecte_chk)

            data_proyectos = json.loads(contabilitat_ajax.AjaxListEstatPrjRespDatos(request, fecha_min, fecha_max, proyectos))
            # totales
            total_concedit = 0
            total_canon_total = 0
            total_ingressos = 0
            total_pendent = 0
            total_despeses = 0
            total_canon_aplicat = 0
            total_compromes = 0
            total_disponible_real = 0
            for dat in data_proyectos:
                total_concedit = total_concedit+dat["concedit"]
                total_canon_total = total_canon_total+dat["canon_total"]
                total_ingressos = total_ingressos+dat["ingressos"]
                total_pendent = total_pendent+dat["pendent"]
                total_despeses = total_despeses+dat["despeses"]
                total_canon_aplicat = total_canon_aplicat+dat["canon_aplicat"]
                total_compromes = total_compromes+dat["compromes"]
                total_disponible_real = total_disponible_real+dat["disponible_real"]
            totales = {"total_concedit":total_concedit,"total_canon_total":total_canon_total,"total_ingressos":total_ingressos,"total_pendent":total_pendent,"total_despeses":total_despeses,"total_canon_aplicat":total_canon_aplicat,"total_compromes":total_compromes,"total_disponible_real":total_disponible_real}
            #######
            # for (index,elemento) in data_proyectos:
            #     elemento=elemento+{""}

            resultado.append({"nom_responsable":nom_resp,"projectes":data_proyectos,"totals":totales})

        context = {'responsables':resultado,"data_max":str(fecha_max),"data_min":str(fecha_min),'titulo': "ESTAT PROJECTES PER RESPONSABLE"} # 'llista_estat_pres': llista_estat_pres,
    except:
        context = {'responsables': [],"data_max":str(fecha_max),"data_min":str(fecha_min), 'titulo': "ESTAT PROJECTES PER RESPONSABLE"}  # 'llista_estat_pres': llista_estat_pres,
    return render(request, 'gestprj/cont_imprimir_resum_estat_prj_resp.html', context)



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
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte', 'percen_iva', 'canon_oficial', 'percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte=projecte[0]# Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = round(concedit + float(importe['import_concedit']),2)

            percen_iva = 0
            if projecte['percen_iva']:
                percen_iva = round(float(projecte['percen_iva']), 2)
            projecte['percen_iva'] = percen_iva

            percen_canon_creaf = 0
            if projecte['percen_canon_creaf']:
                percen_canon_creaf = round(projecte['percen_canon_creaf'], 2)
            projecte['percen_canon_creaf'] = percen_canon_creaf

            canon_oficial = 0
            if projecte['canon_oficial']:
                canon_oficial = round(projecte['canon_oficial'], 2)
            projecte['canon_oficial'] = canon_oficial

            iva = concedit - (concedit / (1 + percen_iva / 100))
            canon = (concedit * float(percen_canon_creaf)) / (100 * (1 + percen_iva / 100))
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

def ListMovimentsCompte(request,compte,data_min,data_max): # AJAX 2 (detall compte)
    resultado=contabilitat_ajax.AjaxListMovimentsCompte(request,compte,data_min,data_max)
    return HttpResponse(resultado, content_type='application/json')

#OJO El AJAX 3 (comprometido de esa cuenta) ESTA ABAJO,EL LISTCOMPROMESCOMPTE

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
            projecte = Projectes.objects.filter(codi_prj=cod_projecte, id_resp=id_resp).values('id_projecte', 'percen_iva', 'canon_oficial','percen_canon_creaf','acronim','id_resp__id_usuari__nom_usuari')  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            projecte=projecte[0]# Ojo aunque devuelva solo un proyecto sigue siendo una lista con diccionario
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte['id_projecte']).values('import_concedit'):
                concedit = round(concedit + float(importe['import_concedit']),2)

            percen_iva = 0
            if projecte['percen_iva']:
                percen_iva = round(float(projecte['percen_iva']), 2)
            projecte['percen_iva'] = percen_iva

            percen_canon_creaf = 0
            if projecte['percen_canon_creaf']:
                percen_canon_creaf = round(projecte['percen_canon_creaf'], 2)
            projecte['percen_canon_creaf'] = percen_canon_creaf

            canon_oficial = 0
            if projecte['canon_oficial']:
                canon_oficial = round(projecte['canon_oficial'], 2)
            projecte['canon_oficial'] = canon_oficial

            iva = concedit - (concedit / (1 + percen_iva / 100))
            canon = (concedit * float(percen_canon_creaf)) / (100 * (1 + percen_iva / 100))
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
    # connections['contabilitat'].MaxVarcharSize  = 1024 * 1024 * 1024
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
    cursor.execute("SELECT CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(varchar(200),CUENTAS.DESCCUE) AS Titulo, CONVERT(varchar,Sum(DEBE))AS TotalDebe, CONVERT(varchar,Sum(HABER))AS TotalHaber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE ( (CUENTAS.CUENTA LIKE '2%%' OR CUENTAS.CUENTA LIKE '6%%' OR CUENTAS.CUENTA LIKE '7%%') AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=%s AND CONVERT(date,FECHA,121)>=%s AND (RIGHT(CUENTAS.CUENTA,5) NOT IN (%s)) ) GROUP BY CUENTAS.CUENTA,CUENTAS.DESCCUE ORDER BY CUENTAS.CUENTA",(fecha_max, fecha_min, lista_codigos))

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

    # Cerramos el cursor
    cursor.close()


    context = {'llista_dades': llista_dades, 'titulo': "COMPTES NO ASSIGNATS A CAP PROJECTE"}
    return render(request, 'gestprj/cont_comptes_no_assignats.html', context)

@login_required(login_url='/menu/')
def ListJustificacionsCabecera(request,fecha_min,fecha_max): # AJAX PARA LAS JUSTIFICACIONES DE LA CABECERA
    resultado=contabilitat_ajax.AjaxListJustificacionsCabecera(request,fecha_min,fecha_max)
    return HttpResponse(resultado, content_type='application/json;')\

@login_required(login_url='/menu/')
def ListAuditoriesCabecera(request,fecha_min,fecha_max): # AJAX PARA LAS JUSTIFICACIONES DE LA CABECERA
    resultado=contabilitat_ajax.AjaxListAuditoriesCabecera(request,fecha_min,fecha_max)
    return HttpResponse(resultado, content_type='application/json;')\


@login_required(login_url='/menu/')
def GenerarInformePeriode(request): # AJAX PARA GENERAR INFORME DE PROYECTOS DURANTE PERIODO (para Agusti)

    projectes = Projectes.objects.all().values("id_projecte","id_resp__codi_resp","codi_prj","acronim","data_inici_prj","data_fi_prj","codi_oficial","titol","acronim","resum","percen_iva","percen_canon_creaf","canon_oficial","id_categoria","resolucio")#.filter(data_fi_prj__gte=datetime.strptime(request.POST["data_ini"], "%d-%m-%Y"), data_fi_prj__lte= datetime.strptime(request.POST["data_fi"], "%d-%m-%Y"))
    resultado = []
    for projecte in projectes:
        data_inici = ""
        if(projecte['data_inici_prj'] != "" and projecte['data_inici_prj'] is not None):
            data_inici = datetime.strptime(str(projecte['data_inici_prj'].date()), "%Y-%m-%d").strftime('%d-%m-%Y')
        data_final = ""
        if (projecte['data_fi_prj'] != "" and projecte['data_fi_prj'] is not None):
            data_final = datetime.strptime(str(projecte['data_fi_prj'].date()), "%Y-%m-%d").strftime('%d-%m-%Y')
        cod_responsable = str(projecte["id_resp__codi_resp"])
        id_usuari_resp = Responsables.objects.get(codi_resp=cod_responsable).id_usuari.id_usuari
        nom_resp = TUsuarisCreaf.objects.get(id_usuari=id_usuari_resp).nom_usuari
        cod_projecte = str(projecte["codi_prj"])
        cod_oficial = str(projecte["codi_prj"])
        titol = projecte["titol"]
        acronim = projecte["acronim"]
        resum = projecte["resum"]
        percen_iva =  projecte["percen_iva"]
        percen_canon_creaf = projecte["percen_canon_creaf"]
        canon_oficial = projecte["canon_oficial"]
        id_projecte = projecte["id_projecte"]
        id_categoria = projecte["id_categoria"]
        #projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp)  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj

        if len(cod_responsable) < 2:
            cod_responsable = "0" + str(cod_responsable)
        if len(cod_projecte) < 3:
            if len(cod_projecte) < 2:
                cod_projecte = "00" + str(cod_projecte)
            else:
                cod_projecte = "0" + str(cod_projecte)

        #####
        centres_participants = CentresParticipants.objects.filter(id_projecte=id_projecte)
        participants_creaf = PersonalCreaf.objects.filter(id_projecte=id_projecte)
        participants_externs = PersonalExtern.objects.filter(id_projecte=id_projecte)

        financadors = Financadors.objects.filter(id_projecte=id_projecte)
        receptors = Receptors.objects.filter(id_projecte=id_projecte)

        # CANON I IVA
        concedit = 0
        for importe in Financadors.objects.filter(id_projecte=id_projecte):
            concedit = round(concedit + float(importe.import_concedit), 2)
        # vienen en la tabla:

        if percen_iva:
            percen_iva = round(float(percen_iva), 4)
        else:
            percen_iva = round(0.0, 4)

        if percen_canon_creaf:
            percen_canon_creaf = round(float(percen_canon_creaf), 4)
        else:
            percen_canon_creaf = round(0.0, 4)

        if canon_oficial:
            canon_oficial = round(float(canon_oficial), 2)
        else:
            canon_oficial = round(0.0, 4)
        # calculados a mano
        if concedit == 0:  # para evitar problemas con la division si es 0
            percen_canon_oficial = 0.00
        else:
            percen_canon_oficial = round(((canon_oficial / concedit) * (100 * (1 + percen_iva / 100))), 4)
        canon_creaf = round(((concedit * float(percen_canon_creaf)) / (100 * (1 + percen_iva / 100))), 2)
        diferencia_per = round((percen_canon_oficial - percen_canon_creaf), 4)
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
        for despesa in Renovacions.objects.filter(id_projecte=id_projecte):
            import_concedit = float(despesa.import_concedit)
            despesa_total_concedit = round(despesa_total_concedit + import_concedit,2)
            iva = round(((import_concedit * percen_iva) / (100 * (1 + percen_iva / 100))), 2)
            despesa_total_iva = round(despesa_total_iva + iva,2)
            canon = round(((import_concedit * percen_canon_creaf) / (100 * (1 + percen_iva / 100))), 2)
            despesa_total_canon = round(despesa_total_canon + canon,2)
            net = round((import_concedit - iva - canon), 2)
            despesa_total_net = round(despesa_total_net + net,2)
            despeses.append(
                {"data_inici": despesa.data_inici, "data_fi": despesa.data_fi, "concedit": import_concedit, "iva": iva,
                 "canon": canon, "net": net})
            # concedit = round(concedit + float(importe.import_concedit),2)

            ####
        #
        # # PRESSUPOST
        # partides = []
        # max_periodes = 0;
        # # al suma de cada periodo
        # totals = [0, 0, 0, 0, 0, 0, 0, 0]
        # total_import = 0
        # partida_total = 0
        #
        # # primero vemos cual es el max de periodos que tiene una de als partidas
        # for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
        #     n_periodes = 0
        #     for periode in PeriodicitatPartida.objects.filter(id_partida=partida.id_partida):
        #         n_periodes = n_periodes + 1
        #         if n_periodes > max_periodes:
        #             max_periodes = n_periodes
        # ######
        #
        # # Despues ponesmos los periodos en cada partida,usamos el max anterior para rellenar con 0 en caso de que haya menos periodos que el maximo
        # for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
        #     periodes = []
        #     total_periode = 0
        #
        #     for index, periode in enumerate(PeriodicitatPartida.objects.filter(id_partida=partida.id_partida)):
        #         total_periode = total_periode + periode.import_field
        #         totals[index] = totals[index] + periode.import_field
        #         periodes.append({"importe": periode.import_field})
        #
        #     if len(periodes) < max_periodes:
        #         for dif in range((max_periodes - len(periodes))):
        #             periodes.append({"importe": 0.00})
        #
        #     totals[max_periodes] = totals[max_periodes] + total_periode
        #
        #     ######
        #
        #     # Si no hay periodos,comprovar si las propias partidas tienen importe:
        #     if not periodes:
        #         total_import = total_import + partida.import_field
        #         partides.append({"concepte": partida.id_concepte_pres.desc_concepte, "import": partida.import_field})
        #     else:
        #         partides.append(
        #             {"concepte": partida.id_concepte_pres.desc_concepte, "periodes": periodes, "total": total_periode})
        #
        #         ######
        #         ########

        es_competitiu = "No competitiu"
        if id_categoria == 2 or id_categoria == 3: #la categoria 3 es la de 'altres convocatories publiques', que tambien cuenta como competitivo
            es_competitiu = "Competitiu ("+TCategoriaPrj.objects.get(id_categoria=id_categoria).desc_categoria+" )"
        else:
            es_competitiu =  "No competitiu ("+TCategoriaPrj.objects.get(id_categoria=id_categoria).desc_categoria+" )"

        # tam_periodes = round(max_periodes/8) #lo dividimos entre 8 para el boostrap,ya que quedan col-md-8 como tamano maximo(hay 2 divs que ocupan 2,el concepto y el total)
        resultado.append({"dades_prj": projecte, "codi_resp": cod_responsable, "codi_prj": cod_projecte, "nom_resp": nom_resp, "data_inici": data_inici, "data_final": data_final, "titol":titol, "acronim":acronim, "resum":resum,
                          'centres_participants': centres_participants, 'participants_creaf': participants_creaf,
                          'participants_externs': participants_externs, 'financadors': financadors,
                          'receptors': receptors, 'canoniva': canoniva, 'despeses': despeses,
                          'total_concedit': despesa_total_concedit, 'total_iva': despesa_total_iva,
                          'total_canon': despesa_total_canon, 'total_net': despesa_total_net, 'es_competitiu':es_competitiu,'resolucio':projecte["resolucio"]})
        # , 'partides': partides,
        #                   'totals_pres': totals, 'max_periodes': range(max_periodes),
        #                   'total_import_pres': total_import})

    if request.POST["tipo"]=="1":
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append([u'Codi projecte', u'Codi responsable', u'Acronim', u'Titol', u'Nom responsable', u"Data inici", u'Data final', u'Competitiu/No competitiu', u'Resolucio',u'Concedit Total', u'Total IVA', u'Total Canon', u'Total Net', u'Resum'])
        #Rellenarlo de datos
        for prj in resultado:
            worksheet.append([prj["codi_prj"],prj["codi_resp"],prj["acronim"],prj["titol"],prj["nom_resp"],str(prj["data_inici"]),str(prj["data_final"]),prj["es_competitiu"],prj["resolucio"],prj["total_concedit"],prj["total_iva"],prj["total_canon"],prj["total_net"],prj["resum"]])
        response = HttpResponse(content=save_virtual_workbook(workbook), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=InformeProjectesPeriode_'+str(request.POST["data_ini"])+'_a_'+str(request.POST["data_fi"])+'.xlsx'
        return response
    else:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="InformeProjectesPeriode_'+str(request.POST["data_ini"])+'_a_'+str(request.POST["data_fi"])+'.csv"'

        writer = csv.writer(response, delimiter=str(";"), dialect='excel')  # quoting=csv.QUOTE_ALL,writer = csv.writer(resultado, delimiter=str(';').encode('utf-8'), dialect='excel', encoding='utf-8') #  quoting=csv.QUOTE_ALL,
        response.write(u'\ufeff'.encode('utf8'))  # IMPORTANTE PARA QUE FUNCIONEN LOS ACENTOS
        writer.writerow([u'Codi projecte', u'Codi responsable', u'Acronim', u'Titol', u'Nom responsable', u"Data inici", u'Data final', u'Competitiu/No competitiu', u'Resolucio',u'Concedit Total', u'Total IVA', u'Total Canon', u'Total Net', u'Resum'])
        for prj in resultado:
            writer.writerow([prj["codi_prj"],prj["codi_resp"],prj["acronim"],prj["titol"],prj["nom_resp"],str(prj["data_inici"]),str(prj["data_final"]),prj["es_competitiu"],prj["resolucio"],prj["total_concedit"],prj["total_iva"],prj["total_canon"],prj["total_net"],prj["resum"]])
        return response
    # resultado=contabilitat_ajax.AjaxListJustificacionsCabecera(request,fecha_min,fecha_max)
    # return HttpResponse(resultado, content_type='application/json;')

@login_required(login_url='/menu/')
def GenerarInformeFinancadorsPeriode(request): # AJAX PARA GENERAR INFORME DE LA FINANCIACION DE PROYECTOS EN X PERIODO(para Agusti)

    projectes = Projectes.objects.filter(data_fi_prj__gte=datetime.strptime(request.POST["data_ini"], "%d-%m-%Y"), data_fi_prj__lte= datetime.strptime(request.POST["data_fi"], "%d-%m-%Y")).values("id_projecte","id_resp__codi_resp","codi_prj","acronim","data_inici_prj","data_fi_prj","codi_oficial","titol","acronim","resum","percen_iva","percen_canon_creaf","canon_oficial","id_categoria","resolucio")
    resultado = []

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="InformeFinancadorsProjectesPeriode_' + str(
        request.POST["data_ini"]) + '_a_' + str(request.POST["data_fi"]) + '.csv"'

    writer = csv.writer(response, delimiter=str(";"),
                        dialect='excel')  # quoting=csv.QUOTE_ALL,writer = csv.writer(resultado, delimiter=str(';').encode('utf-8'), dialect='excel', encoding='utf-8') #  quoting=csv.QUOTE_ALL,
    response.write(u'\ufeff'.encode('utf8'))  # IMPORTANTE PARA QUE FUNCIONEN LOS ACENTOS
    writer.writerow([u'Codi projecte',u'Codi responsable', u'Organisme Financador', u'Import Concedit'])
    for projecte in projectes:
        financadors = Financadors.objects.filter(id_projecte=projecte["id_projecte"]).values("id_organisme__nom_organisme","import_concedit")
        # cod_responsable = str(projecte["id_resp__codi_resp"])
        # cod_projecte = str(projecte["codi_prj"])
        #
        # if len(cod_responsable) < 2:
        #     cod_responsable = "0" + str(cod_responsable)
        # if len(cod_projecte) < 3:
        #     if len(cod_projecte) < 2:
        #         cod_projecte = "00" + str(cod_projecte)
        #     else:
        #         cod_projecte = "0" + str(cod_projecte)
        for financador in financadors:
            writer.writerow([projecte["codi_prj"],projecte["id_resp__codi_resp"],financador["id_organisme__nom_organisme"],financador["import_concedit"]])

    return response


@login_required(login_url='/menu/')
def GenerarInformeReceptorsPeriode(request): # AJAX PARA GENERAR INFORME DE LOS RECEPTORES DE PROYECTOS EN X PERIODO(para Agusti)

    projectes = Projectes.objects.filter(data_fi_prj__gte=datetime.strptime(request.POST["data_ini"], "%d-%m-%Y"), data_fi_prj__lte= datetime.strptime(request.POST["data_fi"], "%d-%m-%Y")).values("id_projecte","id_resp__codi_resp","codi_prj","acronim","data_inici_prj","data_fi_prj","codi_oficial","titol","acronim","resum","percen_iva","percen_canon_creaf","canon_oficial","id_categoria","resolucio")
    resultado = []

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="InformeReceptorsProjectesPeriode_' + str(
        request.POST["data_ini"]) + '_a_' + str(request.POST["data_fi"]) + '.csv"'

    writer = csv.writer(response, delimiter=str(";"),
                        dialect='excel')  # quoting=csv.QUOTE_ALL,writer = csv.writer(resultado, delimiter=str(';').encode('utf-8'), dialect='excel', encoding='utf-8') #  quoting=csv.QUOTE_ALL,
    response.write(u'\ufeff'.encode('utf8'))  # IMPORTANTE PARA QUE FUNCIONEN LOS ACENTOS
    writer.writerow([u'Codi projecte',u'Codi responsable', u'Organisme Receptor', u'Import Rebut'])
    for projecte in projectes:
        receptors = Receptors.objects.filter(id_projecte=projecte["id_projecte"]).values("id_organisme__nom_organisme","import_rebut")
        # cod_responsable = str(projecte["id_resp__codi_resp"])
        # cod_projecte = str(projecte["codi_prj"])
        #
        # if len(cod_responsable) < 2:
        #     cod_responsable = "0" + str(cod_responsable)
        # if len(cod_projecte) < 3:
        #     if len(cod_projecte) < 2:
        #         cod_projecte = "00" + str(cod_projecte)
        #     else:
        #         cod_projecte = "0" + str(cod_projecte)
        for receptor in receptors:
            writer.writerow([projecte["codi_prj"],projecte["id_resp__codi_resp"],receptor["id_organisme__nom_organisme"],receptor["import_rebut"]])

    return response

@login_required(login_url='/menu/')
def GenerarInformeJustificacionsInternesPeriode(request): # AJAX PARA GENERAR INFORME DE LOS RECEPTORES DE PROYECTOS EN X PERIODO(para Agusti)

    projectes = Projectes.objects.filter(data_fi_prj__gte=datetime.strptime(request.POST["data_ini"], "%d-%m-%Y"), data_fi_prj__lte= datetime.strptime(request.POST["data_fi"], "%d-%m-%Y")).values("id_projecte","id_resp__codi_resp","codi_prj","acronim","data_inici_prj","data_fi_prj","codi_oficial","titol","acronim","resum","percen_iva","percen_canon_creaf","canon_oficial","id_categoria","resolucio")
    resultado = []

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="InformeJustificacionsInternesProjectesPeriode_' + str(
        request.POST["data_ini"]) + '_a_' + str(request.POST["data_fi"]) + '.csv"'

    writer = csv.writer(response, delimiter=str(";"),
                        dialect='excel')  # quoting=csv.QUOTE_ALL,writer = csv.writer(resultado, delimiter=str(';').encode('utf-8'), dialect='excel', encoding='utf-8') #  quoting=csv.QUOTE_ALL,
    response.write(u'\ufeff'.encode('utf8'))  # IMPORTANTE PARA QUE FUNCIONEN LOS ACENTOS
    writer.writerow([u'Codi projecte',u'Codi responsable', u'Data Assentament', u'Numero Assentament', u'Descripcio', u'Import'])
    for projecte in projectes:
        justificacions = JustificInternes.objects.filter(id_projecte=projecte["id_projecte"]).values("data_assentament","id_assentament","desc_justif","import_field")
        # cod_responsable = str(projecte["id_resp__codi_resp"])
        # cod_projecte = str(projecte["codi_prj"])
        #
        # if len(cod_responsable) < 2:
        #     cod_responsable = "0" + str(cod_responsable)
        # if len(cod_projecte) < 3:
        #     if len(cod_projecte) < 2:
        #         cod_projecte = "00" + str(cod_projecte)
        #     else:
        #         cod_projecte = "0" + str(cod_projecte)
        for justificacio in justificacions:
            writer.writerow([projecte["codi_prj"],projecte["id_resp__codi_resp"],justificacio["data_assentament"],justificacio["id_assentament"],justificacio["desc_justif"],justificacio["import_field"]])

    return response


@login_required(login_url='/menu/')
def GenerarInformeConcessionsPeriode(request): # AJAX PARA GENERAR INFORME DE LOS RECEPTORES DE PROYECTOS EN X PERIODO(para Agusti)

    projectes = Projectes.objects.filter(data_fi_prj__gte=datetime.strptime(request.POST["data_ini"], "%d-%m-%Y"), data_fi_prj__lte= datetime.strptime(request.POST["data_fi"], "%d-%m-%Y")).values("id_projecte","id_resp__codi_resp","codi_prj","acronim","data_inici_prj","data_fi_prj","codi_oficial","titol","acronim","resum","percen_iva","percen_canon_creaf","canon_oficial","id_categoria","resolucio")
    resultado = []

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="InformeConcessionsRenovacionsProjectesPeriode_' + str(
        request.POST["data_ini"]) + '_a_' + str(request.POST["data_fi"]) + '.csv"'

    writer = csv.writer(response, delimiter=str(";"),
                        dialect='excel')  # quoting=csv.QUOTE_ALL,writer = csv.writer(resultado, delimiter=str(';').encode('utf-8'), dialect='excel', encoding='utf-8') #  quoting=csv.QUOTE_ALL,
    response.write(u'\ufeff'.encode('utf8'))  # IMPORTANTE PARA QUE FUNCIONEN LOS ACENTOS
    writer.writerow([u'Codi projecte',u'Codi responsable',u'Data Inici', u'Data Fi', u'Import Concedit'])
    for projecte in projectes:
        renovacions = Renovacions.objects.filter(id_projecte=projecte["id_projecte"]).values("data_inici","data_fi","import_concedit")
        # cod_responsable = str(projecte["id_resp__codi_resp"])
        # cod_projecte = str(projecte["codi_prj"])
        #
        # if len(cod_responsable) < 2:
        #     cod_responsable = "0" + str(cod_responsable)
        # if len(cod_projecte) < 3:
        #     if len(cod_projecte) < 2:
        #         cod_projecte = "00" + str(cod_projecte)
        #     else:
        #         cod_projecte = "0" + str(cod_projecte)
        for renovacio in renovacions:
            writer.writerow([projecte["codi_prj"],projecte["id_resp__codi_resp"],renovacio["data_inici"],renovacio["data_fi"],renovacio["import_concedit"]])

    return response


@login_required(login_url='/menu/')
def ListProjectesResponsableCabecera(request): # AJAX PARA LOS PROYECTOS POR RESPONSABLES DE LA CABECERA

    #pillamos los proyectos abiertos(se ve que en el gestor antiguo es lo que hace)
    projectes = Projectes.objects.filter(id_estat_prj__id_estat_prj=1).values("id_projecte","id_resp__codi_resp","codi_prj","acronim") #los proyectos totales
    resultado=[]
    investigadores = {}  # diccionario

    for projecte in projectes:
        if int(projecte["id_resp__codi_resp"]) not in investigadores:
            investigadores[int(projecte["id_resp__codi_resp"])]=int(projecte["id_resp__codi_resp"])

    investigadores = sorted(investigadores.values())
    for inv in investigadores:
        proyectos = [] # los proyectos de ese investigador
        if inv==94:#####Excepcion para el caso de SEVERO y el Retana
            nom_investigador="Javier Retana(SEVERO)";
        else:
            nom_investigador=Responsables.objects.get(codi_resp=inv).id_usuari.nom_usuari


        #id_investigador = str(Responsables.objects.get(codi_resp=inv).id_usuari.id_usuari)
        for projecte in projectes:
            if inv==projecte["id_resp__codi_resp"]:
                codi=str(projecte["id_resp__codi_resp"])+"-"+str(projecte["codi_prj"])
                nom=projecte["acronim"]
                entitats=""
                for entitat in Financadors.objects.filter(id_projecte=projecte["id_projecte"]).values("id_organisme__nom_organisme"):
                    entitats=entitats+entitat["id_organisme__nom_organisme"]+" - "
                proyectos.append({"codi":codi,"nom":nom,"entitats":entitats})

        resultado.append({"codi_investigador":inv,"nom_responsable":nom_investigador,"projectes":proyectos})

    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

@login_required(login_url='/menu/')
def ListUsuarisXarxaSenseAssignar(request): # AJAX PARA LOS USUARIOS XARXA QUE NO ESTAN ASIGNADOS A UN USUARIO CREAF
    resultado = []
    usuarios_no_asignados = TUsuarisCreaf.objects.exclude(id_usuari__in=TUsuarisXarxa.objects.all().values_list('id_usuari',flat=True))

    for usuario in usuarios_no_asignados:
        resultado.append({"id": float(usuario.id_usuari),"nom_usuari": usuario.nom_usuari})

    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

@login_required(login_url='/menu/')
def AfegirUsuarisXarxaSenseAssignar(request):  # AJAX PARA LOS USUARIOS XARXA QUE NO ESTAN ASIGNADOS A UN USUARIO CREAF
    try:
        id=request.POST["id"]
        nom_usuari = request.POST["nom_usuari"]
        # nom_creaf = resquest.POST["nom_creaf"]
        u = TUsuarisXarxa.objects.create(id_usuari=id,nom_xarxa=nom_usuari)
        u.save()
        return HttpResponse('')
    except:
        return HttpResponse('Error.', status=401)
# # OBTENER LOS DATOS DE UNA FACTURA
# @login_required(login_url='/menu/')
# def DatosFactura(request): # AJAX PARA LAS JUSTIFICACIONES DE LA CABECERA
#     resultado=contabilitat_ajax.AjaxDatosFactura(request)
#     return HttpResponse(resultado, content_type='application/json;')

############################################################ PCI

@login_required(login_url='/menu/')
def ListPciCabecera(request,id_grup,fecha_min_pci,fecha_max_pci): # AJAX PARA LOS PROYECTOS CON X ORGANIZACION FINANCIERA (PCI CABECERA)
    resultado=contabilitat_ajax.AjaxListPciCabecera(request,id_grup,fecha_min_pci,fecha_max_pci)
    return HttpResponse(resultado, content_type='application/json;')

class ListGrupsPci(generics.ListAPIView): # AJAX PARA LOS GRUPOS PCI
    serializer_class = GestGrupsPciSerializer

    def get_queryset(self):
        return GrupsPci.objects.all()

class GestGrupsPci(viewsets.ModelViewSet):  # gestionar grups pci
    queryset = GrupsPci.objects.all()
    serializer_class = GestGrupsPciSerializer

############ ORGANISMOS DE DICHO GRUPO PCI
class ListOrganismesGrupPci(generics.ListAPIView): # AJAX PARA LOS ORGANISMOS DE UN GRUPO PCI
    serializer_class = GestOrganismesGrupPciSerializer

    def get_queryset(self):
        _id_grup = self.kwargs['id_grup']
        return Organismes_GrupsPci.objects.filter(id_grup=_id_grup)

class GestOrganismeGrupPci(viewsets.ModelViewSet):  # gestionar ORGANISMOS GRUPO PCI
    queryset = Organismes_GrupsPci.objects.all()
    serializer_class = GestGrupsPci

##################################################### IMPUTACIÓ INGRESSOS
@login_required(login_url='/menu/')
def BuscarImputacioIngressos(request,id_grup,id_estat,fecha_min_imputacio,fecha_max_imputacio): # AJAX PARA LOS PROYECTOS CON X ORGANIZACION FINANCIERA (PCI CABECERA)
    resultado=contabilitat_ajax.AjaxImputacioIngressos(request,id_grup,id_estat,fecha_min_imputacio,fecha_max_imputacio)
    return HttpResponse(resultado, content_type='application/json;')



@login_required(login_url='/menu/')
def AfegirOrganismeGrupPci(request): # AJAX PARA LOS PROYECTOS CON X ORGANIZACION FINANCIERA (PCI CABECERA)
    try:
        id_grup= GrupsPci.objects.get(id_grup=request.POST["id_grup"])
        id_organisme=TOrganismes.objects.get(id_organisme=request.POST["id_organisme"])
        # nom_creaf = resquest.POST["nom_creaf"]
        u = Organismes_GrupsPci.objects.create(id_grup=id_grup,id_organisme=id_organisme)
        u.save()
        return HttpResponse('')
    except:
        return HttpResponse('Error.', status=401)

# ORGANISMES #################
def ListGrupsPciSelect(request): # AJAX
    resultado = contabilitat_ajax.AjaxListGrupsPciSelect()
    return HttpResponse(resultado, content_type='application/json;')

# @login_required(login_url='/menu/')
# def ListOrganismesGrupPci(request,id_grup):  # ORGANISMOS DE UN GRUPO PCI
#     resultado = []
#     #usuarios_no_asignados = TUsuarisCreaf.objects.exclude(id_usuari__in=TUsuarisXarxa.objects.all().values_list('id_usuari',flat=True))
#
#     organismes_grup = Organismes_GrupsPci.objects.all(id_grup=id_grup).values("id_organisme","id_organisme__nom_organisme")
#     for organisme in organismes_grup:
#         resultado.append({"id_organisme":organisme.id_organisme,"nom_organisme": organisme.id_organisme__nom_organisme})
#
#     resultado = json.dumps(resultado)
#     return HttpResponse(resultado, content_type='application/json;')
#
