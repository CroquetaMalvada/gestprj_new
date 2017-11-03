from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connections
from django.core import serializers
from gestprj.models import Projectes, TCategoriaPrj, TOrganismes, CentresParticipants, PersonalExtern, TUsuarisExterns, PersonalCreaf, TUsuarisCreaf, JustificPersonal, TFeines, Financadors, Receptors, JustificInternes, Renovacions, TConceptesPress, Pressupost, PeriodicitatPres, PeriodicitatPartida, Desglossaments, ClausDiferenCompte, JustificProjecte, AuditoriesProjecte, Responsables
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
    GestAuditoriesSerializer
from gestprj import pk,consultes_cont
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

    # llista_projectes = Projectes.objects.all()
    # for projecte in llista_projectes:
    #     if projecte.id_resp is not None:
    #         if projecte.id_resp.id_usuari is not None:
    #             print projecte.id_resp.id_usuari.nom_usuari
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
    organismos = TOrganismes.objects.all().order_by('nom_organisme')
    resultado=[]
    for organismo in organismos:
        resultado.append({'id':str(organismo.id_organisme),'nom': organismo.nom_organisme})

    resultado = json.dumps(resultado)
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
# def ListPersonalCreaf(request):
#     personal = PersonalCreaf.objects.all().order_by('id_usuari__nom_usuari') # AJAX
#     resultado=[]
#     for pers in personal:
#         resultado.append({'id':str(smo.id_organisme),'nom': organismo.nom_organisme})
#
#     resultado = json.dumps(resultado)
#     return HttpResponse(resultado, content_type='application/json;')

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

    # perso = PersonalCreaf.objects.get(id_perso_creaf=)
    # if(perso.es_justificacio=0):


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

    # def snippet_list(request):
    #         return Response(GestPressupostSerializer.data)


# PERIODICITAT PRESSUPOST

class ListPeriodicitatPres(generics.ListCreateAPIView):
    # def snippet_list(request):  OJO QUE ESTO PUEDE SERVIR PARA MAS ADELANTE
    # """
    # List all snippets, or create a new snippet.
    # """
    # if request.method == 'GET':
    #     snippets = Snippet.objects
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

    # def snippet_list(request):
    #     if request.method == 'POST':
    #         return Response(GestPeriodicitatPresSerializer.data)


# PERIODICITAT PARTIDA

class ListPeriodicitatPartida(generics.ListCreateAPIView):
    serializer_class = GestPeriodicitatPartidaSerializer

    def get_queryset(self):
        if self.kwargs['id_partida'] is None:
            return PeriodicitatPartida.objects.all()
        else:
            _id_partida = self.kwargs['id_partida']
            return PeriodicitatPartida.objects.filter(id_partida=_id_partida)

            # def get_queryset(self):
            #     if self.kwargs['id_partida'] is None:
            #         return PeriodicitatPartida.objects.all()
            #     else:
            #         _id_partida = self.kwargs['id_partida']
            #         return PeriodicitatPartida.objects.filter(id_partida=_id_partida)


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

            # def get_queryset(self):
            #     if self.kwargs['id_partida'] is None:
            #         return PeriodicitatPartida.objects.all()
            #     else:
            #         _id_partida = self.kwargs['id_partida']
            #         return PeriodicitatPartida.objects.filter(id_partida=_id_partida)


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



################################ CONTABILIDAD!!!!

# VERSION CONTABILIDAD
def json_vacio(request):
    return HttpResponse([{}], content_type='application/json;')

@login_required(login_url='/menu/')
def list_projectes_cont(request): #simplemente carga la template
    # if request.user.groups.filter(name="Admins gestprj").exists():#si el usuario es un admin,muetra todos los proyectos
    #     llista_projectes = Projectes.objects.all()
    #     llista_responsables = Responsables.objects.all()
    # else:#sino solo muestra SUS proyectos
    #     responsable = usuari_a_responsable(request)
    #     llista_responsables = responsable
    #
    #     if responsable is not None:
    #         llista_projectes = Projectes.objects.filter(id_resp__id_resp=responsable.id_resp)
    #     else:
    #         llista_projectes = None


    context = { 'titulo': "CONTABILITAT"} # 'llista_projectes': llista_projectes ,
    return render(request, 'gestprj/contabilitat.html', context)

#AJAX PARA RELLENAR RESPONSABLES
@login_required(login_url='/menu/')
def ListResponsablesCont(request):
    if request.user.groups.filter(name="Admins gestprj").exists():#si el usuario es un admin,muetra todos los responsables
        llista_responsables = Responsables.objects.all().values('id_usuari__nom_usuari','id_resp')
        resultado = []
        for responsable in llista_responsables:
            nom = responsable['id_usuari__nom_usuari']
            id_resp = str(responsable['id_resp'])
            resultado.append({'Nom': nom, 'Id_resp': id_resp})
        resultado = json.dumps(resultado)
        return HttpResponse(resultado, content_type='application/json;')

    else:#sino solo saldra el
        responsable = usuari_a_responsable(request)
        resultado = []
        if responsable is not None:
            nom = responsable.id_usuari.nom_usuari
            id_resp = str(responsable.id_resp)
            resultado.append({'Nom': nom, 'Id_resp': id_resp})
            resultado = json.dumps(resultado)
            return HttpResponse(resultado, content_type='application/json;')
        else:
            return HttpResponse([{}], content_type='application/json')

#AJAX PARA RELLENAR PROYECTOS
@login_required(login_url='/menu/')
def ListProjectesCont(request):
    if request.user.groups.filter(name="Admins gestprj").exists():#si el usuario es un admin,muetra todos los proyectos
        llista_projectes = Projectes.objects.select_related('id_resp').select_related('id_estat_prj').all().values('codi_prj','id_resp__codi_resp','id_estat_prj__desc_estat_prj','acronim','id_resp__id_resp')
        # prefetch_related("id_resp__id_estat_prj")
        resultado = []
        for projecte in llista_projectes:
            codi = ""
            # codi_resp=int(projecte.id_resp.codi_resp)
            codi_prj=str(projecte['codi_prj'])
            estat = projecte['id_estat_prj__desc_estat_prj']
            acronim = projecte['acronim']
            id_resp = str(projecte['id_resp__id_resp'])
            codi_resp = str(projecte['id_resp__codi_resp'])

            if len(codi_prj) < 3:
                if len(codi_prj) < 2:
                    codi = "00" + codi_prj
                else:
                    codi = "0" + codi_prj
            else:
                codi = str(codi_prj)

            if len(codi_resp) < 2:
                codi = "0" + codi_resp + codi
            else:
                codi = codi_resp + codi


            resultado.append({'Codi': codi, 'Estat': estat, 'Acronim': acronim, 'Id_resp': id_resp})
        resultado = json.dumps(resultado)
        return HttpResponse(resultado, content_type='application/json;')

    else:#sino solo muestra SUS proyectos
        responsable = usuari_a_responsable(request)
        resultado = []
        #quitar este if cuando el gestor este acabado
        if(request.user.username=="josepantoni"):
            llista_projectes = Projectes.objects.filter(id_resp__id_resp="8").values('codi_prj','id_resp__codi_resp','id_estat_prj__desc_estat_prj','acronim','id_resp__id_resp')
            responsable="josepanotni"
        else:
            llista_projectes = Projectes.objects.filter(id_resp__id_resp=responsable.id_resp).values('codi_prj','id_resp__codi_resp','id_estat_prj__desc_estat_prj','acronim','id_resp__id_resp')

        if responsable is not None:
            for projecte in llista_projectes:
                codi = ""
                # codi_resp=int(projecte.id_resp.codi_resp)
                codi_prj = str(projecte['codi_prj'])
                estat = projecte['id_estat_prj__desc_estat_prj']
                acronim = projecte['acronim']
                id_resp = str(projecte['id_resp__id_resp'])
                codi_resp = str(projecte['id_resp__codi_resp'])

                if len(codi_prj) < 3:
                    if len(codi_prj) < 2:
                        codi = "00" + codi_prj
                    else:
                        codi = "0" + codi_prj
                else:
                    codi = str(codi_prj)

                if len(codi_resp) < 2:
                    codi = "0" + codi_resp + codi
                else:
                    codi = codi_resp + codi

                resultado.append({'Codi': codi, 'Estat': estat, 'Acronim': acronim, 'Id_resp': id_resp})
            resultado = json.dumps(resultado)
            return HttpResponse(resultado, content_type='application/json;')
        else:
            return HttpResponse([{}], content_type='application/json')

    #resultado = '[{"Nom": "Dani", "Codi_resp": "1"},{"Nom": "minidani", "Codi_resp": "2"}]'

# DADES PROJECTE

@login_required(login_url='/menu/')
def cont_dades(request):

    projectes = request.POST
    llista_dades = consultes_cont.ContDades(projectes)

    context = {'llista_dades': llista_dades, 'titulo': "FITXA DADES"}
    return render(request, 'gestprj/cont_dades.html', context)

# ESTAT PRESUPOSTARI

@login_required(login_url='/menu/')
def cont_estat_pres(request):
    try:
        projectes = request.POST
        fecha_min = datetime.strptime(projectes["data_min"], "%d-%m-%Y")
        fecha_max = datetime.strptime(projectes["data_max"], "%d-%m-%Y")
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

            # llista_estat_pres = consultes_cont.ContEstatPres(projectes)

        context = { 'projectes':resultado,'titulo': "ESTAT PRESSUPOSTARI"} # 'llista_estat_pres': llista_estat_pres,
    except:
        context = {'projectes': [], 'titulo': "ESTAT PRESSUPOSTARI"}  # 'llista_estat_pres': llista_estat_pres,
    return render(request, 'gestprj/cont_estat_pres.html', context)



@login_required(login_url='/menu/') # AJAX 1 (SE RELLENAN LAS TABLAS)
def ListEstatPresDatos(request,datos):

    cursor = connections['contabilitat'].cursor()
    if (datos.count("_")== 3): #en la pos 0 se obtiene el id del periodo,la 1 y 2 son las fechas del periodo y en la 3 el codigo entero)
        partidas = []
        id_periode = datos.split("_")[0]
        data_min_periode = datos.split("_")[1]
        data_max_periode = datos.split("_")[2]
        codigo_entero = datos.split("_")[3]
        tipos_partida = {}
        for partidaperio in PeriodicitatPartida.objects.filter(id_periodicitat=id_periode).values('id_partida','id_partida__id_partida','id_partida__id_concepte_pres__desc_concepte','import_field'):  # partida de x periodo
            id_partida = partidaperio['id_partida']
            desc_partida = partidaperio['id_partida__id_concepte_pres__desc_concepte']
            pressupostat = float(partidaperio['import_field'])
            if desc_partida not in tipos_partida:
                tipos_partida[desc_partida] = {"desc_partida": desc_partida, "pressupostat": float(0), "gastat": float(0),"saldo": float(0), 'id_partida': str(id_partida), 'codigo_entero': codigo_entero, 'fecha_min': data_min_periode, 'fecha_max': data_max_periode}
            ### para obtener el gastat
            gastat = 0
            cuenta = 0
            for compte in Desglossaments.objects.filter(id_partida=partidaperio['id_partida__id_partida']).values('compte','id_compte','id_compte__clau_compte'):
                cod_compte = str(compte['compte'])
                if cod_compte is None:
                    cod_compte = "0000"
                # primer_digito=str(cod_compte)[0] # solo son cuentas contables los que empiezan por 6 y 2
                # if primer_digito =='6' or primer_digito =='2' :
                if len(cod_compte) < 4:
                    if len(cod_compte) < 3:
                        if len(cod_compte) < 2:
                            cod_compte = cod_compte + "%%%"
                        else:
                            cod_compte = cod_compte + "%%"
                    else:
                        cod_compte = cod_compte + "%"

                if compte['id_compte']:
                    clau = str(compte['id_compte__clau_compte'])

                # Ojo parece que se necesitan 3 espacios en el codigo de centrocoste2,puede ser por la importacion que hicieron los de erp?los datos nuevos introducidos tambien tienen esos 3 espacios?
                # OJO UTILIZAR FECHAS?
                cursor.execute("SELECT DEBE,HABER,DESCAPU FROM __ASIENTOS WHERE(  CENTROCOSTE2='   '+(?) AND ( CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) AND TIPAPU='N'  AND IDCUENTA IN (SELECT IDCUENTA FROM CUENTAS WHERE CUENTA LIKE (?)+'%' AND CUENTA NOT LIKE 6296+(?) ) ) ",[codigo_entero, data_max_periode, data_min_periode, cod_compte, codigo_entero])
                cuentacont = dictfetchall(cursor)
                if cuentacont:
                    for cont in cuentacont:
                        if cont["DEBE"] is None:
                            cont["DEBE"] = 0
                        if cont["HABER"] is None:
                            cont["HABER"] = 0
                        gastat = gastat + (Decimal(cont["DEBE"] - cont["HABER"]))

            saldo = pressupostat - float(gastat)  # pasamos datos a float ya que los decimal no los pilla bien el json
            #partidas.append({"desc_partida": desc_partida, "pressupostat": float(pressupostat), "gastat": float(gastat),"saldo": float(saldo), 'id_partida': str(id_partida), 'codigo_entero': codigo_entero})
            tipos_partida[desc_partida]["pressupostat"]=float(tipos_partida[desc_partida]["pressupostat"]+pressupostat)
            tipos_partida[desc_partida]["gastat"] = float(tipos_partida[desc_partida]["gastat"] + float(gastat))
            tipos_partida[desc_partida]["saldo"] = float(tipos_partida[desc_partida]["saldo"] + saldo)
        for partida in tipos_partida:
            partidas.append(tipos_partida[partida])
        resultado = json.dumps(partidas)
        return HttpResponse(resultado, content_type='application/json;')
            # codigo_final = cod_compte + codigo_entero  # en realidad seria de 9 digitos pero como en la consulta ponemos un 6 o un delante es de 8


    if (datos.count("_")==4):  # si no es un periodo sino el total(en este caso en la pos 0 se obtiene el id del prj,la 1 y 2 son la FECHAS DEL PROYECTO y en la 3 el codigo entero)
        partidas = []
        for partida in Pressupost.objects.filter(id_projecte=datos.split("_")[0]).values('id_partida','id_concepte_pres__desc_concepte','import_field'):  # partidas de proyecto
            id_partida = partida['id_partida']
            desc_partida = partida['id_concepte_pres__desc_concepte']
            pressupostat = float(partida['import_field'])
            id_prj = datos.split("_")[0]
            data_min = datos.split("_")[1]
            data_max = datos.split("_")[2]
            codigo_entero = datos.split("_")[3]

            ### para obtener el gastat
            gastat = 0
            for compte in Desglossaments.objects.filter(id_partida=id_partida).values('compte'):
                cod_compte = str(compte['compte'])
                if cod_compte is None:
                    cod_compte = "0000"
                # primer_digito=str(cod_compte)[0] # solo son cuentas contables los que empiezan por 6 y 2
                # if primer_digito =='6' or primer_digito =='2' :
                if len(cod_compte) < 4:
                    if len(cod_compte) < 3:
                        if len(cod_compte) < 2:
                            cod_compte = cod_compte + "%%%"
                        else:
                            cod_compte = cod_compte + "%%"
                    else:
                        cod_compte = cod_compte + "%"

                # Ojo parece que se necesitan 3 espacios en el codigo de centrocoste2,puede ser por la importacion que hicieron los de erp?los datos nuevos introducidos tambien tienen esos 3 espacios?
                # OJO UTILIZAR FECHAS?
                cursor.execute("SELECT DEBE,HABER,DESCAPU FROM __ASIENTOS WHERE CENTROCOSTE2='   '+(?) AND ( CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) AND TIPAPU='N' AND IDCUENTA IN (SELECT IDCUENTA FROM CUENTAS WHERE CUENTA LIKE (?)+'%' ) ",[codigo_entero, data_max, data_min, cod_compte])  # AND ( FECHA<'2017-01-01 00:00:00.000' )
                cuentacont = dictfetchall(cursor)
                if cuentacont:
                    for cont in cuentacont:
                        if cont["DEBE"] is None:
                            cont["DEBE"] = 0
                        if cont["HABER"] is None:
                            cont["HABER"] = 0
                        gastat = gastat + (Decimal(cont["DEBE"] - cont["HABER"]))

            saldo = pressupostat - float(gastat)  # pasamos datos a float ya que los decimal no los pilla bien el json
            partidas.append({"desc_partida": desc_partida, "pressupostat": float(pressupostat), "gastat": float(gastat),"saldo": float(saldo), 'id_partida': str(id_partida), 'codigo_entero': codigo_entero, 'fecha_min': data_min, 'fecha_max': data_max})
        resultado = json.dumps(partidas)
        return HttpResponse(resultado, content_type='application/json;')
    # projectes = request.POST
    # fecha_min = datetime.strptime(projectes["data_min"], "%d-%m-%Y")
    # fecha_max = datetime.strptime(projectes["data_max"], "%d-%m-%Y")

    # resultado = consultes_cont.ContEstatPres(datos)
    # resultado = json.dumps(resultado)
    return HttpResponse([], content_type='application/json;')


def ListDespesesCompte(request,id_partida,cod,data_min,data_max): # AJAX 2 (SE MUESTRAN LOS DATOS
    if int(id_partida) != 0:
        fetch = consultes_cont.DespesesCompte(id_partida,cod,data_min,data_max)
        # resultado = json.dumps(fetch, ensure_ascii=False)
        resultado = json.dumps(fetch)
        return HttpResponse(resultado, content_type='application/json;')
    else:
        return HttpResponse([{}], content_type='application/json')

# DESPESES PROJECTE

@login_required(login_url='/menu/')
def cont_despeses(request):

    projectes = request.POST
    llista_despeses = consultes_cont.ContDespeses(projectes)

    context = {'llista_despeses': llista_despeses, 'titulo': "LLISTA DE DESPESES"}
    return render(request, 'gestprj/cont_despeses.html', context)
    # return HttpResponse([{}])

# INGRESOS PROJECTE

@login_required(login_url='/menu/')
def cont_ingresos(request):

    projectes = request.POST
    llista_ingresos = consultes_cont.ContIngresos(projectes)

    context = {'llista_ingresos': llista_ingresos, 'titulo': "LLISTA DE INGRESOS"}
    return render(request, 'gestprj/cont_ingresos.html', context)

@login_required(login_url='/menu/')
def cont_resum_estat_prj(request):

    projectes = request.POST
    llista_dades = consultes_cont.ResumEstatProjectes(projectes)  # Ojo que este hace un return de 2 arrays,uno con los datos(llsita_dades[0]) y otro con los totales(llista_dades[1])

    context = {'llista_dades': llista_dades[0],'totals': llista_dades[1],'titulo': "RESUM ESTAT PROJECTES"}
    return render(request, 'gestprj/cont_resum_estat_prj.html', context)

@login_required(login_url='/menu/')
def cont_estat_prj_resp(request):

    # projectes = request.POST
    # llista_dades = consultes_cont.EstatProjectesResp(projectes)
    try:
        projectes = request.POST
        fecha_min = datetime.strptime(projectes["data_min"], "%d-%m-%Y")
        fecha_max = datetime.strptime(projectes["data_max"], "%d-%m-%Y")
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

            resultado.append({"nom_responsable":nom_resp,"data_max":str(fecha_max),"data_min":str(fecha_min),"projectes":proyectos})

        context = {'responsables':resultado,'titulo': "ESTAT PROJECTES PER RESPONSABLE"} # 'llista_estat_pres': llista_estat_pres,
    except:
        context = {'responsables': [], 'titulo': "ESTAT PROJECTES PER RESPONSABLE"}  # 'llista_estat_pres': llista_estat_pres,
    return render(request, 'gestprj/cont_RESUM_estat_prj_resp.html', context)

@login_required(login_url='/menu/')
def ListEstatPrjRespDatos(request,fecha_min,fecha_max,proyectos): # AJAX1(SE RELLENAN LAS TABLAS)
    cursor = connections['contabilitat'].cursor()
    resultado=[]
    for proyecto in str(proyectos).split(","):
        cod_responsable = proyecto.split("-")[0]
        id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
        cod_projecte = proyecto.split("-")[1]
        projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp)  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
        nom_resp = Responsables.objects.get(codi_resp=cod_responsable).id_usuari.nom_usuari
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
            percen_canon_oficial = ((projecte.canon_oficial / concedit) * (100 * (1 + projecte.percen_iva / 100)))

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
                       "(SELECT CONVERT(varchar,Sum(DEBE))AS ingressosD, CONVERT(varchar,Sum(HABER))AS ingressosH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND CUENTAS.CUENTA LIKE '7%' AND CUENTAS.CUENTA NOT LIKE '79%' AND TIPAPU='N' AND CONVERT(date,FECHA,121)<=(?))) AS ingressos,"
                       "(SELECT CONVERT(varchar,Sum(DEBE))AS despesesD, CONVERT(varchar,Sum(HABER))AS despesesH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '6%' OR CUENTAS.CUENTA LIKE '2%') AND CUENTAS.CUENTA NOT LIKE '6296'+(?) AND TIPAPU='N' AND CONVERT(date,FECHA,121)<=(?))) AS despeses,"
                       "(SELECT CONVERT(varchar,Sum(DEBE))AS canonD, CONVERT(varchar,Sum(HABER))AS canonH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '79%' OR CUENTAS.CUENTA LIKE '6296%') AND TIPAPU='N' AND CONVERT(date,FECHA,121)<=(?))) AS canon",
                       [codigo_entero, fecha_max, codigo_entero, codigo_entero, fecha_max, codigo_entero, fecha_max])

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

        resultado.append({"codi":codigo_entero,"nom":projecte.acronim,"concedit":concedit,"canon_total":canon_total,"ingressos":ingressos,"pendent":pendent,"despeses":despeses,"canon_aplicat":canon_aplicat,"disponible_real":disponible_real})
    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

@login_required(login_url='/menu/')
def cont_resum_fitxa_major_prj(request): #RESUM PER PARTIDES

    try:
        projectes = request.POST
        fecha_min = datetime.strptime(projectes["data_min"], "%d-%m-%Y")
        fecha_max = datetime.strptime(projectes["data_max"], "%d-%m-%Y")
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

    # projectes = request.POST
    # llista_dades = consultes_cont.ResumFitxaMajorProjectes(projectes)
    #
    # context = {'llista_dades': llista_dades, 'titulo': "RESUM PER PARTIDES"}
    # return render(request, 'gestprj/cont_resum_fitxa_major_prj.html', context)

@login_required(login_url='/menu/')
def ListResumFitxaMajorPrjDatos(request,fecha_min,fecha_max,codigo): #AJAX1(SE RELLENAN LAS TABLAS)
    cursor = connections['contabilitat'].cursor()
    resultado=[]
    comptes = {}
    ##### Para extraer el objeto proyecto y el codigo:
    cod_responsable = codigo.split("-")[0]
    id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
    cod_projecte = codigo.split("-")[1]
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
    ##### Cuentas:
    concedit = 0
    for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
        concedit = concedit + importe.import_concedit

    iva = concedit - (concedit / (1 + projecte.percen_iva / 100))
    canon = (concedit * projecte.percen_canon_creaf) / (100 * (1 + projecte.percen_iva / 100))
    net_disponible = concedit - iva - canon
    #####

    # obtener las cuentas de x proyecto
    cursor.execute("SELECT CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(varchar(200),CUENTAS.DESCCUE) AS Titulo, CONVERT(varchar,Sum(DEBE))AS TotalDebe, CONVERT(varchar,Sum(HABER))AS TotalHaber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE ( CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '2%' OR CUENTAS.CUENTA LIKE '6%' OR CUENTAS.CUENTA LIKE '7%') AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) GROUP BY CUENTAS.CUENTA,CUENTAS.DESCCUE ORDER BY CUENTAS.CUENTA",[codigo_entero, fecha_max, fecha_min])
    # cursor.execute("SELECT TOP 100 PERCENT Apuntes.Cuenta, Plan_cuentas.Titulo, Sum(Apuntes.Debe) AS TotalDebe, Sum(Apuntes.Haber) AS TotalHaber FROM Plan_cuentas LEFT JOIN Apuntes ON (Plan_cuentas.Cuenta = Apuntes.Cuenta) WHERE ( (Plan_cuentas.Nivel=0) AND (((Apuntes.Cuenta) LIKE '2%'+(?))OR((Apuntes.Cuenta) LIKE '6%'+(?) )OR((Apuntes.Cuenta) LIKE '7%'+(?))) AND ((Apuntes.Diario)='0' OR (Apuntes.Diario)='4' OR (Apuntes.Diario)='1') AND ((Apuntes.Fecha)>=CONVERT(date, (?),105) AND (Apuntes.Fecha)<=CONVERT(date, (?),105))) GROUP BY Apuntes.Cuenta, Plan_cuentas.Titulo ORDER BY Apuntes.Cuenta",[codigo_entero,codigo_entero,codigo_entero,fecha_min,fecha_max])
    projectfetch = dictfetchall(cursor)  # un cursor.description tambien sirve

    ##### Para ir restando el saldo a medida que salen gastos:
    total_disponible = 0  # Ojo ES EL SALDO INICIAL ****SIEMPRE ES 0???????
    total_debe = 0
    total_haber = 0
    for prjfet in projectfetch:
        if prjfet["TotalDebe"] == None:
            prjfet["TotalDebe"] = 0
        if prjfet["TotalHaber"] == None:
            prjfet["TotalHaber"] = 0
        # por cada cuenta,guardar los detalles/movimientos de la misma
        cursor.execute("SELECT CONVERT(VARCHAR,FECHA,105)as Fecha, SUBSTRING(CONVERT(VARCHAR,NUMAPUNTE), 6, 4) AS Asiento,  CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(NVARCHAR(100),DESCAPU) AS Descripcion, CONVERT(varchar,DEBE)AS Debe, CONVERT(varchar,HABER)AS Haber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CUENTAS.CUENTA=(?) AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) ORDER BY cast(FECHA as date)",[prjfet["Cuenta"], fecha_max, fecha_min])
        # cursor.execute("SELECT TOP 100 PERCENT Fecha, Asiento, Cuenta, Descripcion, Debe, Haber FROM Apuntes WHERE (Cuenta=(?) AND (Diario='0' OR Diario='4' OR Diario='1') AND ((Apuntes.Fecha)>=CONVERT(date, (?),105) AND (Apuntes.Fecha)<=CONVERT(date, (?),105))) ORDER BY cast(Fecha as date)",[prjfet["Cuenta"],fecha_min,fecha_max])
        comptes[prjfet["Cuenta"]] = dictfetchall(cursor)

        total_debe = total_debe + float(prjfet["TotalDebe"])
        total_haber = total_haber + float(prjfet["TotalHaber"])
        total_disponible = round(total_disponible - float(prjfet["TotalDebe"]) + float(prjfet["TotalHaber"]), 2)

        if total_disponible < 0.1 and total_disponible > -0.1:  # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
            total_disponible = 0

        if total_debe < 0.1 and total_debe > -0.1:
            total_debe = 0

        if total_haber < 0.1 and total_haber > -0.1:
            total_haber = 0

        prjfet["Total_disponible"] = total_disponible
        prjfet["Codigo_entero"] = codigo_entero
        prjfet["Codigo_cuenta"] = prjfet["Cuenta"][:4]

        resultado.append({"codigo_entero":codigo_entero,"compte":prjfet["Cuenta"],"descripcio":prjfet["Titulo"],"despesa":prjfet["TotalDebe"],"ingres":prjfet["TotalHaber"],"saldo":total_disponible,"fecha_min":fecha_min,"fecha_max":fecha_max})

    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

def ListMovimentsCompte(request,compte,data_min,data_max):
    if compte != "0":
        fetch = consultes_cont.MovimentsCompte(compte,data_min,data_max)
        resultado = json.dumps(fetch)
        return HttpResponse(resultado, content_type='application/json')
    else:
        return HttpResponse([{}], content_type='application/json')


@login_required(login_url='/menu/')
def cont_fitxa_major_prj(request): # INGRESSOS I DESPESES (FITXA MAJOR PRJ)

    try:
        projectes = request.POST
        fecha_min = datetime.strptime(projectes["data_min"], "%d-%m-%Y")
        fecha_max = datetime.strptime(projectes["data_max"], "%d-%m-%Y")
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

    # projectes = request.POST
    # llista_dades = consultes_cont.FitxaMajorProjectes(projectes)
    #
    # context = {'llista_dades': llista_dades, 'titulo': "INGRESSOS I DESPESES"}
    # return render(request, 'gestprj/cont_fitxa_major_prj.html', context)

@login_required(login_url='/menu/')
def ListFitxaMajorPrjDatos(request,fecha_min,fecha_max,codigo): # AJAX1(SE RELLENAN LAS TABLAS)
    cursor = connections['contabilitat'].cursor()
    resultado=[]

    ##### Para extraer el objeto proyecto y el codigo:
    cod_responsable = codigo.split("-")[0]
    id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
    cod_projecte = codigo.split("-")[1]
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

    ##### OJO que para ir restando el saldo hay que devolver los resultados ordenados por la fecha,para ello he tenido que modificar el ORDER BY
    cursor.execute("SELECT CENTROCOSTE,CENTROCOSTE2,NUMAPUNTE,CONVERT(VARCHAR,FECHA,105)as Fecha, SUBSTRING(CONVERT(VARCHAR,NUMAPUNTE), 6, 4) AS Asiento,  CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(NVARCHAR(100),CUENTAS.DESCCUE) AS Desc_cuenta,CONVERT(NVARCHAR(100),DESCAPU) AS Descripcion, CONVERT(varchar,DEBE)AS Debe, CONVERT(varchar,HABER)AS Haber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '7%' OR CUENTAS.CUENTA LIKE '2%' OR CUENTAS.CUENTA LIKE '6%') AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) ORDER BY cast(FECHA as date)",[codigo_entero, fecha_max, fecha_min])
    # cursor.execute("SELECT TOP 100 PERCENT CONVERT(VARCHAR,Fecha,105) as Fecha, Asiento, Cuenta, Descripcion, Debe, Haber FROM  Apuntes WHERE ((Diario='0' OR Diario='1' OR Diario='4') AND ((Cuenta LIKE '2%'+(?)) OR (Cuenta LIKE '6%'+(?)) OR (Cuenta LIKE '7%'+(?))) AND ((Fecha >=CONVERT(date, (?),105)) AND (Fecha<=CONVERT(date, (?),105)))) ORDER BY cast(Fecha as date)",[codigo_entero, codigo_entero, codigo_entero, fecha_min, fecha_max])
    projectfetch = dictfetchall(cursor)  # un cursor.description tambien sirve

    ##### Para ir restando el saldo a medida que salen gastos:
    total_caja = 0  # ES EL SALDO INICIAL ****SIEMPRE ES 0???????
    total_debe = 0
    total_haber = 0
    for prjfet in projectfetch:
        if prjfet["Debe"] == None:
            prjfet["Debe"] = 0
        if prjfet["Haber"] == None:
            prjfet["Haber"] = 0

        # prjfet["Saldo_caja"] = round(total_caja + (float(prjfet["Haber"]) - float(prjfet["Debe"])), 2)
        # total_debe = total_debe + float(prjfet["Debe"])
        # total_haber = total_haber + float(prjfet["Haber"])
        # total_caja = float(prjfet["Saldo_caja"])
        # OJO CENTROCOSTE3 SIEMPRE ES NULO,PERO NO DESCARTAR QUE EN UN FUTUR PUEDA TENER ALGUN VALOR,NUMAPUNTE ES MUY IMPROTANTE PESE A NO SER UNA FK!!!
        cursor.execute("SELECT OBSERVACIONES FROM CABEFACC WHERE CENTROCOSTE=(?) AND CENTROCOSTE2=(?) AND NUMAPUNTE=(?)",[prjfet["CENTROCOSTE"], prjfet["CENTROCOSTE2"], prjfet["NUMAPUNTE"]])

        observacion = cursor.fetchall()
        if observacion:
            if observacion[0][0] is None:
                prjfet["Observaciones"] = "Sense observacions."
            else:
                prjfet["Observaciones"] = observacion[0][0]
        else:
            prjfet["Observaciones"] = "Sense observacions."

        # if total_caja < 0.1 and total_caja > -0.1:  # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
        #     total_disponible = 0
        #
        # if total_debe < 0.1 and total_debe > -0.1:
        #     total_debe = 0
        #
        # if total_haber < 0.1 and total_haber > -0.1:
        #     total_haber = 0


        resultado.append({"data":prjfet["Fecha"],"asiento":prjfet["Asiento"],"compte":prjfet["Cuenta"],"desc_compte":prjfet["Desc_cuenta"],"descripcio":prjfet["Descripcion"],"Observaciones":prjfet["Observaciones"],"despesa":prjfet["Debe"],"ingres":prjfet["Haber"]})
    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

@login_required(login_url='/menu/')
def cont_resum_estat_canon(request):

    projectes = request.POST
    llista_dades = consultes_cont.ResumEstatCanon(projectes)

    context = {'llista_dades': llista_dades, 'titulo': "RESUM ESTAT CANON PROJECTES PER RESPONSABLE"}
    return render(request, 'gestprj/cont_resum_estat_canon.html', context)

@login_required(login_url='/menu/')
def cont_comptes_no_assignats(request):

    projectes = request.POST
    llista_dades = consultes_cont.ComptesNoAssignats(projectes)

    context = {'llista_dades': llista_dades, 'titulo': "COMPTES NO ASSIGNATS A CAP PROJECTE"}
    return render(request, 'gestprj/cont_comptes_no_assignats.html', context)

@login_required(login_url='/menu/')
def ListJustificacionsCabecera(request,fecha_min,fecha_max): # AJAX PARA LAS JUSTIFICACIONES DE LA CABECERA
    resultado=[]
    fecha_min = datetime.strptime(fecha_min, "%d-%m-%Y")
    fecha_max = datetime.strptime(fecha_max, "%d-%m-%Y")
    for justificacio in JustificProjecte.objects.filter(data_justificacio__gte=fecha_min, data_justificacio__lte=fecha_max):
        codigo_entero=str(justificacio.id_projecte.id_resp.codi_resp)+str("-")+str(justificacio.id_projecte.codi_prj)
        resultado.append({"data":str(justificacio.data_justificacio),"codi":codigo_entero,"nom":justificacio.id_projecte.acronim,"responsable":justificacio.id_projecte.id_resp.id_usuari.nom_usuari,"periode":"Del "+str(justificacio.data_inici_periode)+" al "+str(justificacio.data_fi_periode),"observacions":justificacio.comentaris})
    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')