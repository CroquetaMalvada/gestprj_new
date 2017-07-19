from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from gestprj.models import Projectes, TCategoriaPrj, TOrganismes, CentresParticipants, PersonalExtern, TUsuarisExterns, \
    PersonalCreaf, TUsuarisCreaf, JustificPersonal, TFeines, Financadors, Receptors, JustificInternes, Renovacions, \
    TConceptesPress, Pressupost, PeriodicitatPres, PeriodicitatPartida, Desglossaments, ClausDiferenCompte, \
    JustificProjecte, AuditoriesProjecte, Responsables
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
# Create your views here.
@login_required(login_url='/menu/')
# @user_passes_test(lambda u: u.groups.filter(name="Admins gestprj").count() == 0, login_url="/logout/" )
def index(request):
    return HttpResponseRedirect('/llista_projectes/')
    # return HttpResponse("Hello, world.")


@login_required(login_url='/menu/')
# @user_passes_test(es_usuario_valido,login_url='/menu/')

# @user_passes_test(not_in_student_group, login_url="/logout/" )
# @user_passes_test(lambda u: u.groups.filter(name="Admins gestprj").count() == 0, login_url="/logout/" )
def list_projectes(request):
    # llista_projectes = TUsuarisXarxa.objects.all()
    # usuarixarxa = usuari_xarxa_a_user(request)
    if request.user.groups.filter(name="Admins gestprj").exists():#si el usuario es un admin,muetra todos los proyectos
        llista_projectes = Projectes.objects.all()
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


# VERSION CONTABILIDAD
@login_required(login_url='/menu/')
def list_projectes_cont(request):
    if request.user.groups.filter(name="Admins gestprj").exists():#si el usuario es un admin,muetra todos los proyectos
        llista_projectes = Projectes.objects.all()
    else:#sino solo muestra SUS proyectos
        responsable = usuari_a_responsable(request)

        if responsable is not None:
            llista_projectes = Projectes.objects.filter(id_resp__id_resp=responsable.id_resp)
        else:
            llista_projectes = None

    #anadir el codigo de responsable de cada proyecto
    # for projecte in llista_projectes:
    #     projecte.id_resp.codi_resp = int(projecte.id_resp.codi_resp)
    #     projecte.codi_prj = int(projecte.codi_prj)

    context = {'llista_projectes': llista_projectes,'llista_responsables': Responsables.objects.all(), 'titulo': "CONTABILITAT"}
    return render(request, 'gestprj/contabilitat.html', context)


@login_required(login_url='/menu/')
@user_passes_test(es_admin,login_url='/welcome/')
def new_project(request, id=None):
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
        id = pk.generaPkProjecte()

    form = ProjectesForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()  # \/ pasar el id por url no sirve,hay que ponerlo en la del form
        return render(request, 'gestprj/projecte_nou.html',
                      {'form': form, 'titulo': 'EDITANT PROJECTE', 'categories': categories, 'organismes': organismes,
                       'tipus_feines': feines, 'partides': partides, 'claus_comptes': claus_comptes,
                       'id_projecte': id, 'errorprojecte':False})  # , 'id_projecte':1534
    else:
        if nuevo:  # Si esta mal pero es nuevo
            return render(request, 'gestprj/projecte_nou.html',
                          {'form': form, 'titulo': 'NOU PROJECTE', 'categories': categories, 'organismes': organismes,
                           'tipus_feines': feines, 'partides': partides, 'claus_comptes': claus_comptes,
                           'id_projecte': id, 'nuevo': True, 'errorprojecte':True})

    # Si esta mal pero se esta editando:
    return render(request, 'gestprj/projecte_nou.html',
                  {'form': form, 'titulo': 'EDITANT PROJECTE', 'categories': categories, 'organismes': organismes,
                   'tipus_feines': feines, 'partides': partides, 'claus_comptes': claus_comptes,
                   'id_projecte': id, 'errorprojecte':True})


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



# @login_required(login_url='/menu/')
# def update_project(request):
#         # if this is a POST request we need to process the form data
#
#     categories = TCategoriaPrj.objects.all()
#     organismes = TOrganismes.objects.all()
#
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         # validez = 0
#
#         form = ProjectesForm(request.POST)
#
#         # form = ProjectesForm(request.POST)
#         # check whether it's valid:
#
#         if form.is_valid():
#             project = form.save()
#             # if request.POST['id_projecte'] == "-1":
#             #     #Proyecto nuevo
#             #     project.id_projecte = pk.generaPkProjecte()
#             #     project.save()
#             # else:
#             #     #Editar proyecto
#             #     project.update()
#             # ####
#             # # foreach guardando los centros participantes anadidos
#
#             # project = form.save()
#             # form.save()
#             # Projectes.objects.update_or_create(id_projecte=project.pk, **form.cleaned_data)
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             # return HttpResponseRedirect('/mod_projecte/')
#             return render(request, 'gestprj/projecte_nou.html', {'form': form,'titulo':'EDITANT PROJECTE', 'categories':categories, 'id_projecte':project.pk})# , 'id_projecte':1534
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = ProjectesForm()
#
#     return render(request, 'gestprj/projecte_nou.html', {'form': form,'titulo':'NOU PROJECTE', 'categories':categories})# , 'id_projecte':1534


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

class ListTOrganismes(viewsets.ModelViewSet):  # todos los organismos
    queryset = TOrganismes.objects.all()
    serializer_class = GestTOrganismesSerializer


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

    projectes = request.POST
    llista_estat_pres = consultes_cont.ContEstatPres(projectes)

    context = {'llista_estat_pres': llista_estat_pres, 'titulo': "ESTAT PRESSUPOSTARI"}
    return render(request, 'gestprj/cont_estat_pres.html', context)

def ListDespesesCompte(request,id_partida,cod,data_min,data_max):
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

    projectes = request.POST
    llista_dades = consultes_cont.EstatProjectesResp(projectes)

    context = {'llista_dades': llista_dades,'titulo': "ESTAT PROJECTES PER RESPONSABLE"}
    return render(request, 'gestprj/cont_resum_estat_prj_resp.html', context)


@login_required(login_url='/menu/')
def cont_resum_fitxa_major_prj(request):

    projectes = request.POST
    llista_dades = consultes_cont.ResumFitxaMajorProjectes(projectes)

    context = {'llista_dades': llista_dades, 'titulo': "RESUM ESTAT MAJOR PROJECTES"}
    return render(request, 'gestprj/cont_resum_fitxa_major_prj.html', context)

def ListMovimentsCompte(request,compte,data_min,data_max):
    if compte != "0":
        fetch = consultes_cont.MovimentsCompte(compte,data_min,data_max)
        resultado = json.dumps(fetch)
        return HttpResponse(resultado, content_type='application/json')
    else:
        return HttpResponse([{}], content_type='application/json')


@login_required(login_url='/menu/')
def cont_fitxa_major_prj(request):

    projectes = request.POST
    llista_dades = consultes_cont.FitxaMajorProjectes(projectes)

    context = {'llista_dades': llista_dades, 'titulo': "RESUM ESTAT MAJOR PROJECTES"}
    return render(request, 'gestprj/cont_fitxa_major_prj.html', context)

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