from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connections
from django.core import serializers
from gestprj.models import Projectes, TCategoriaPrj, TOrganismes, CentresParticipants, PersonalExtern, TUsuarisExterns, PersonalCreaf, TUsuarisCreaf, JustificPersonal, TFeines, Financadors, Receptors, JustificInternes, Renovacions, TConceptesPress, Pressupost, PeriodicitatPres, PeriodicitatPartida, Desglossaments, ClausDiferenCompte, JustificProjecte, AuditoriesProjecte, Responsables, TUsuarisXarxa, PrjUsuaris,User
from django.db.models import Q
from gestprj.forms import UsuariXarxaForm
from gestprj.forms import ProjectesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django_auth_ldap.config import LDAPGroupType,LDAPSearch
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
import ldap
from ldap_groups import ADGroup
import json

GROUP_DN = "cn=Users,dc=creaf,dc=uab,dc=es"

def dictfetchall(cursor):
    # Devuelve todos los campos de cada row como una lista
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def AjaxListProjectesSelect():
    proyectos = Projectes.objects.all().order_by('acronim')
    resultado=[]
    for proyecto in proyectos:
        resultado.append({'id':str(proyecto.id_projecte),'acronim': proyecto.acronim})

    resultado = json.dumps(resultado)
    return resultado

def AjaxListOrganismesSelect():
    organismos = TOrganismes.objects.all().order_by('nom_organisme')
    resultado=[]
    for organismo in organismos:
        resultado.append({'id':str(organismo.id_organisme),'nom': organismo.nom_organisme})

    resultado = json.dumps(resultado)
    return resultado


def AjaxListUsuarisXarxaSelect():
    usuarisCreaf = ADGroup("cn=CREAFEOUSERS,cn=Users,dc=creaf,dc=uab,dc=es").get_member_info()
    usuarisXarxa = TUsuarisXarxa.objects.all().values("id_usuari_xarxa","nom_xarxa").order_by("nom_xarxa") # .values_list("nom_xarxa",flat=True) # .order_by("nom_xarxa")

    resultado=[]
    for usuari in usuarisXarxa:
            resultado.append({'id': str(usuari["id_usuari_xarxa"]), 'nom': str(usuari["nom_xarxa"])})
    # DESCOMENTAR ESTO MAS ADELANTE
    # usuaris=User.objects.all().values_list("username",flat=True)
    # # de momento que solo se vean los usuarios loginados
    # for usuari in usuarisXarxa:
    #     if usuari["nom_xarxa"] in usuaris:
    #         resultado.append({'id': str(usuari["id_usuari_xarxa"]), 'nom': str(usuari["nom_xarxa"])})



    resultado = json.dumps(resultado)
    return resultado

def AjaxListUsuarisExternsSelect():
    usuarisExterns = TUsuarisExterns.objects.all().values("id_usuari_extern","nom_usuari_extern","id_organisme__nom_organisme").order_by("nom_usuari_extern") # .values_list("nom_xarxa",flat=True) # .order_by("nom_xarxa")

    resultado=[]
    for usuari in usuarisExterns:
            resultado.append({'id': str(usuari["id_usuari_extern"]), 'nom': usuari["nom_usuari_extern"],'organisme':usuari["id_organisme__nom_organisme"]})


    resultado = json.dumps(resultado)
    return resultado

def AjaxListResponsablesCont(request):
    if request.user.groups.filter(name="Admins gestprj").exists():#si el usuario es un admin,muetra todos los responsables
        llista_responsables = Responsables.objects.all().values('id_usuari__nom_usuari','id_resp')
        resultado = []
        for responsable in llista_responsables:
            nom = responsable['id_usuari__nom_usuari']
            id_resp = str(responsable['id_resp'])
            resultado.append({'Nom': nom, 'Id_resp': id_resp})
        resultado = json.dumps(resultado)
        return resultado
    else:#sino solo saldra el
        responsable = usuari_a_responsable(request)
        resultado = []
        if responsable is not None:
            nom = responsable.id_usuari.nom_usuari
            id_resp = str(responsable.id_resp)
            resultado.append({'Nom': nom, 'Id_resp': id_resp})
            resultado = json.dumps(resultado)
            return resultado
        else:
            return [{}]

def AjaxListProjectesCont(request):
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
        return resultado

    else:#sino solo muestra SUS proyectos o LOS QUE TENGA PERMISO
        responsable = usuari_a_responsable(request)
        resultado = []

        # quitar este if cuando el gestor este acabado
        if (request.user.username == "josepantoni"):
            llista_projectes = Projectes.objects.filter(id_resp__id_resp="8").values('codi_prj','id_resp__codi_resp','id_estat_prj__desc_estat_prj','acronim', 'id_resp__id_resp')
            responsable = "josepanotni"
        else:
            if responsable is not None:
                llista_projectes = Projectes.objects.filter(id_resp__id_resp=responsable.id_resp).values('codi_prj','id_resp__codi_resp','id_estat_prj__desc_estat_prj','acronim','id_resp__id_resp')
            else:
                llista_projectes = []

        llista_projectes = list(llista_projectes)
        # Comprobar si el usuario tiene permiso para ver otros proyectos y anadirlos a la llista_projectes
        for permiso in PrjUsuaris.objects.all():
            nom_xarxa = TUsuarisXarxa.objects.get(id_usuari_xarxa=permiso.id_usuari_xarxa.id_usuari_xarxa).nom_xarxa
            if (request.user.username == nom_xarxa):
                projectes=list(Projectes.objects.filter(id_projecte=permiso.id_projecte.id_projecte).values('codi_prj','id_resp__codi_resp','id_estat_prj__desc_estat_prj','acronim','id_resp__id_resp'))
                llista_projectes.append(projectes[0])

        # Comprobar si el investigador esta colaborando en otros proyectos *Ojo esto esta comentado porque de momento todos los permisos se asignan manualmente
        # if responsable is not None:
        #     for proyecto in PersonalCreaf.objects.filter(id_usuari=responsable.id_usuari).values('id_projecte'):
        #         prj=list(Projectes.objects.filter(id_projecte=proyecto["id_projecte"]).values('codi_prj','id_resp__codi_resp','id_estat_prj__desc_estat_prj','acronim','id_resp__id_resp'))
        #         llista_projectes.append(prj[0])

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
        return resultado



def AjaxListEstatPresDatos(request,datos):

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
        return resultado
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
            data_min = datetime.strptime(data_min, "%d-%m-%Y")
            data_max = datetime.strptime(data_max, "%d-%m-%Y")
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
            partidas.append({"desc_partida": desc_partida, "pressupostat": float(pressupostat), "gastat": float(gastat),"saldo": float(saldo), 'id_partida': str(id_partida), 'codigo_entero': codigo_entero, 'fecha_min': str(data_min), 'fecha_max': str(data_max)})
        resultado = json.dumps(partidas)
        return resultado

    return []


def AjaxListDespesesCompte(request,id_partida,cod,data_min,data_max):
    if int(id_partida) != 0:
        fetch = consultes_cont.DespesesCompte(id_partida,cod,data_min,data_max)
        # resultado = json.dumps(fetch, ensure_ascii=False)
        resultado = json.dumps(fetch)
        return resultado
    else:
        return [{}]

def AjaxListDespesesDatos(request,fecha_min,fecha_max,codigo):

    fecha_min = datetime.strptime(fecha_min, "%d-%m-%Y")
    fecha_max = datetime.strptime(fecha_max, "%d-%m-%Y")
    # fecha_min = projectes["data_min"]
    # fecha_max = projectes["data_max"]
    cursor = connections['contabilitat'].cursor()
    resultado = []
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
    ##### Cuentas:
    concedit = 0
    for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
        concedit = concedit + importe.import_concedit
    iva = concedit - (concedit / (1 + projecte.percen_iva / 100))
    canon = (concedit * projecte.percen_canon_creaf) / (100 * (1 + projecte.percen_iva / 100))
    net_disponible = concedit - iva - canon

    concedit = round(concedit, 2)
    iva = round(iva, 2)
    canon = round(canon, 2)
    net_disponible = round(net_disponible, 2)
    #####

    # 105 en el convert equivale al dd-mm-yyyy
    cursor.execute("SELECT CONVERT(VARCHAR,FECHA,105)as Fecha, SUBSTRING(CONVERT(VARCHAR,NUMAPUNTE), 6, 4) AS Asiento,  CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(VARCHAR,TEXTO) as Clau, CONVERT(NVARCHAR(200),DESCAPU) AS Documento,CONVERT(NVARCHAR(100),DESCAPU) AS Descripcion, CONVERT(varchar,DEBE)AS Debe, CONVERT(varchar,HABER)AS Haber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '2%' OR CUENTAS.CUENTA LIKE '6%') AND CUENTAS.CUENTA  NOT LIKE  '6296'+(?) AND TIPAPU='N' AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) ORDER BY cast(FECHA as date)",[codigo_entero, codigo_entero, fecha_max, fecha_min])
    # SELECT CONVERT(varchar, FECHA,105) AS Fecha, SUBSTRING(CONVERT(VARCHAR,NUMAPUNTE), 6, 4) AS Asiento, CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(NVARCHAR(100),DESCAPU) AS Descripcion, CONVERT(varchar,DEBE)AS Debe FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE CENTROCOSTE2='   '+(?) AND ( CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) )  AND __ASIENTOS.IDCUENTA IN (SELECT IDCUENTA FROM CUENTAS WHERE CUENTA LIKE (?)+'%' AND CUENTA  NOT LIKE 6296+(?) ) ",[codigo_entero,data_max_periode,data_min_periode, cod_compte, codigo_entero])
    # cursor.execute(
    #     "SELECT TOP 100 PERCENT CONVERT(VARCHAR,Fecha,105)as Data, Asiento, Documento, Cuenta, Opc1, Opc3, Descripcion, Opc2, Debe, Haber FROM  Apuntes WHERE ((Diario='0' OR Diario='1' OR Diario='4') AND (((Cuenta LIKE '2%'+(?)) OR (Cuenta LIKE '6%'+(?))) AND (Cuenta  NOT LIKE  '6296'+(?))) AND ((Fecha >= CONVERT(date,(?),105)) AND (Fecha<=CONVERT(date,(?),105)))) ORDER BY cast(Fecha as date)",
    #     [codigo_entero, codigo_entero, codigo_entero, fecha_min, fecha_max])
    projectfetch = dictfetchall(cursor)  # un cursor.description tambien sirve

    # cursor.execute("SELECT CONVERT(varchar,DEBE)AS Debe FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND CUENTAS.CUENTA LIKE '470%'  AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) ORDER BY cast(FECHA as date)",[codigo_entero, fecha_max, fecha_min])
    # net_disponible = dictfetchall(cursor) # un cursor.description tambien sirve
    saldo_disponible = float(net_disponible)

    total_despeses = 0
    for prjfet in projectfetch:
        if prjfet["Haber"] == None:
            prjfet["Haber"] = 0

        if prjfet["Debe"] == None:
            prjfet["Debe"] = 0
        # else:

        prjfet["Debe"] = float(prjfet["Debe"]) - float(
            prjfet["Haber"])  # optimizar mas adelante al hacer lo del rendimiento
        saldo_disponible = saldo_disponible - float(prjfet["Debe"])
        total_despeses = total_despeses + float(prjfet["Debe"])

        if saldo_disponible < 0.1 and saldo_disponible > -0.1:  # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
            saldo_disponible = 0

        prjfet["saldo_disponible"] = saldo_disponible

        #####
        # total_disponible = saldo_disponible

        resultado.append(
            {"data": prjfet["Fecha"], "asiento": prjfet["Asiento"], "compte": prjfet["Cuenta"], "clau": prjfet["Clau"],
             "descripcio": prjfet["Descripcion"], "despesa": prjfet["Debe"],
             "saldo_disponible": prjfet["saldo_disponible"]})
    resultado = json.dumps(resultado)
    return resultado

def AjaxListIngresosDatos(request,fecha_min,fecha_max,codigo):
    fecha_min = datetime.strptime(fecha_min, "%d-%m-%Y")
    fecha_max = datetime.strptime(fecha_max, "%d-%m-%Y")
    cursor = connections['contabilitat'].cursor()
    resultado = []
    ##### Para extraer el objeto proyecto y el codigo:
    cod_responsable = codigo.split("-")[0]
    id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
    cod_projecte = codigo.split("-")[1]
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
    # canon = (concedit * projecte.percen_canon_creaf) / (100 * (1 + projecte.percen_iva / 100))
    net_disponible = concedit - iva  # Ojo que este no usa canon

    concedit = round(concedit, 2)
    iva = round(iva, 2)
    # canon = round(canon, 2)
    net_disponible = round(net_disponible, 2)
    #####

    # 105 en el convert equivale al dd-mm-yyyy
    cursor.execute(
        "SELECT CONVERT(VARCHAR,FECHA,105)as Fecha, SUBSTRING(CONVERT(VARCHAR,NUMAPUNTE), 6, 4) AS Asiento,  CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(NVARCHAR(100),DESCAPU) AS Descripcion, CONVERT(varchar,DEBE)AS Debe, CONVERT(varchar,HABER)AS Haber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND CUENTAS.CUENTA LIKE '7%' AND CUENTAS.CUENTA  NOT LIKE  '79%' AND CUENTAS.CUENTA  NOT LIKE  '6296'+(?) AND TIPAPU='N' AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) ORDER BY cast(FECHA as date)",
        [codigo_entero, codigo_entero, fecha_max, fecha_min])
    # cursor.execute("SELECT TOP 100 PERCENT CONVERT(VARCHAR,Fecha,105)as Data, Asiento, Cuenta, Descripcion, Debe, Haber FROM  Apuntes WHERE ((Diario='0' OR Diario='1' OR Diario='4') AND (Cuenta LIKE '7%'+(?)) AND (Cuenta  NOT LIKE  '6296'+(?)) AND ((Fecha >= CONVERT(date,(?),105)) AND (Fecha<=CONVERT(date,(?),105)))) ORDER BY cast(Fecha as date)",[codigo_entero, codigo_entero, fecha_min, fecha_max])
    projectfetch = dictfetchall(cursor)  # un cursor.description tambien sirve

    ##### Para ir restando el saldo pendiente a medida que salen ingresos:
    saldo_pendiente = float(net_disponible)
    total_ingresos = 0
    for prjfet in projectfetch:
        if prjfet["Haber"] == None:
            prjfet["Haber"] = 0
        else:
            saldo_pendiente = saldo_pendiente - float(prjfet["Haber"])
            total_ingresos = total_ingresos + float(prjfet["Haber"])

        if saldo_pendiente < 0.1 and saldo_pendiente > -0.1:  # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
            saldo_pendiente = 0
        prjfet["saldo_pendiente"] = saldo_pendiente

        #####
        # total_pendiente = saldo_pendiente

        # resultado.append({"dades_prj": projecte, "ingresos": projectfetch, "concedit": concedit,"iva_percen": float(projecte.percen_iva), "iva": iva, "net_disponible": net_disponible,"saldo": saldo_pendiente, "total_ingresos": total_ingresos,"codi_resp": cod_responsable, "codi_prj": cod_projecte})
        resultado.append({"data": prjfet["Fecha"], "asiento": prjfet["Asiento"], "compte": prjfet["Cuenta"],
                          "descripcio": prjfet["Descripcion"], "ingres": prjfet["Haber"], "saldo": saldo_pendiente})

    resultado = json.dumps(resultado)
    return resultado

def AjaxListEstatPrjRespDatos(request,fecha_min,fecha_max,proyectos):
    fecha_min = datetime.strptime(fecha_min, "%d-%m-%Y")
    fecha_max = datetime.strptime(fecha_max, "%d-%m-%Y")
    cursor = connections['contabilitat'].cursor()
    resultado = []
    for proyecto in str(proyectos).split(","):
        cod_responsable = proyecto.split("-")[0]
        id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
        cod_projecte = proyecto.split("-")[1]
        projecte = Projectes.objects.get(codi_prj=cod_projecte,
                                         id_resp=id_resp)  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
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
            percen_canon_oficial = 0.0000
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
        despeses = round(despesesD - despesesH, 2)  # OJO! que los que en los que estan tancats las despesas suelen coincir con el net_disponible,pero siempre es despesesD-H
        canon_aplicat = round(canonD - canonH, 2)
        disponible_caixa = round(ingressos - despeses - canon_aplicat, 2)
        disponible_real = round(concedit - iva - canon_total - despeses,
                                2)  # OJO esta ok,solo que como algunos importes salen x100 tiene un valor elevado.
        pendent = round(abs(concedit - iva - ingressos), 2)

        resultado.append(
            {"codi": codigo_entero, "nom": projecte.acronim, "concedit": concedit, "canon_total": canon_total,
             "ingressos": ingressos, "pendent": pendent, "despeses": despeses, "canon_aplicat": canon_aplicat,
             "disponible_real": disponible_real})
    resultado = json.dumps(resultado)
    return resultado

def AjaxListResumFitxaMajorPrjDatos(request,fecha_min,fecha_max,codigo):
    fecha_min = datetime.strptime(fecha_min, "%d-%m-%Y")
    fecha_max = datetime.strptime(fecha_max, "%d-%m-%Y")
    cursor = connections['contabilitat'].cursor()
    resultado = []
    comptes = {}
    ##### Para extraer el objeto proyecto y el codigo:
    cod_responsable = codigo.split("-")[0]
    id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
    cod_projecte = codigo.split("-")[1]
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
    ##### Cuentas:
    concedit = 0
    for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
        concedit = concedit + importe.import_concedit

    iva = concedit - (concedit / (1 + projecte.percen_iva / 100))
    canon = (concedit * projecte.percen_canon_creaf) / (100 * (1 + projecte.percen_iva / 100))
    net_disponible = concedit - iva - canon
    #####

    # obtener las cuentas de x proyecto
    cursor.execute(
        "SELECT CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(varchar(200),CUENTAS.DESCCUE) AS Titulo, CONVERT(varchar,Sum(DEBE))AS TotalDebe, CONVERT(varchar,Sum(HABER))AS TotalHaber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE ( CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '2%' OR CUENTAS.CUENTA LIKE '6%' OR CUENTAS.CUENTA LIKE '7%') AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) GROUP BY CUENTAS.CUENTA,CUENTAS.DESCCUE ORDER BY CUENTAS.CUENTA",
        [codigo_entero, fecha_max, fecha_min])
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
        cursor.execute(
            "SELECT CONVERT(VARCHAR,FECHA,105)as Fecha, SUBSTRING(CONVERT(VARCHAR,NUMAPUNTE), 6, 4) AS Asiento,  CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(NVARCHAR(100),DESCAPU) AS Descripcion, CONVERT(varchar,DEBE)AS Debe, CONVERT(varchar,HABER)AS Haber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CUENTAS.CUENTA=(?) AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) ORDER BY cast(FECHA as date)",
            [prjfet["Cuenta"], fecha_max, fecha_min])
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

        resultado.append({"codigo_entero": codigo_entero, "compte": prjfet["Cuenta"], "descripcio": prjfet["Titulo"],
                          "despesa": prjfet["TotalDebe"], "ingres": prjfet["TotalHaber"], "saldo": total_disponible,
                          "fecha_min": str(fecha_min), "fecha_max": str(fecha_max)})

    resultado = json.dumps(resultado)
    return resultado

def AjaxListMovimentsCompte(request,compte,data_min,data_max):
    if compte != "0":
        fetch = consultes_cont.MovimentsCompte(compte,data_min,data_max)
        resultado = json.dumps(fetch)
        return resultado
    else:
        return [{}]

def AjaxListFitxaMajorPrjDatos(request,fecha_min,fecha_max,codigo):
    fecha_min = datetime.strptime(fecha_min, "%d-%m-%Y")
    fecha_max = datetime.strptime(fecha_max, "%d-%m-%Y")
    cursor = connections['contabilitat'].cursor()
    resultado = []

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
    cursor.execute(
        "SELECT CENTROCOSTE,CENTROCOSTE2,NUMAPUNTE,CONVERT(VARCHAR,FECHA,105)as Fecha, SUBSTRING(CONVERT(VARCHAR,NUMAPUNTE), 6, 4) AS Asiento,  CONVERT(VARCHAR,CUENTAS.CUENTA) AS Cuenta, CONVERT(NVARCHAR(100),CUENTAS.DESCCUE) AS Desc_cuenta,CONVERT(NVARCHAR(100),DESCAPU) AS Descripcion, CONVERT(varchar,DEBE)AS Debe, CONVERT(varchar,HABER)AS Haber FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '7%' OR CUENTAS.CUENTA LIKE '2%' OR CUENTAS.CUENTA LIKE '6%') AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?) AND CONVERT(date,FECHA,121)>=(?) ) ORDER BY cast(FECHA as date)",
        [codigo_entero, fecha_max, fecha_min])
    projectfetch = dictfetchall(cursor)  # un cursor.description tambien sirve

    for prjfet in projectfetch:
        if prjfet["Debe"] == None:
            prjfet["Debe"] = 0
        if prjfet["Haber"] == None:
            prjfet["Haber"] = 0

        # OJO CENTROCOSTE3 SIEMPRE ES NULO,PERO NO DESCARTAR QUE EN UN FUTUR PUEDA TENER ALGUN VALOR,NUMAPUNTE ES MUY IMPROTANTE PESE A NO SER UNA FK!!!
        cursor.execute(
            "SELECT OBSERVACIONES FROM CABEFACC WHERE CENTROCOSTE=(?) AND CENTROCOSTE2=(?) AND NUMAPUNTE=(?)",
            [prjfet["CENTROCOSTE"], prjfet["CENTROCOSTE2"], prjfet["NUMAPUNTE"]])

        observacion = cursor.fetchall()
        if observacion:
            if observacion[0][0] is None:
                prjfet["Observaciones"] = "Sense observacions."
            else:
                prjfet["Observaciones"] = observacion[0][0]
        else:
            prjfet["Observaciones"] = "Sense observacions."
        resultado.append({"data": prjfet["Fecha"], "asiento": prjfet["Asiento"], "compte": prjfet["Cuenta"],
                          "desc_compte": prjfet["Desc_cuenta"], "descripcio": prjfet["Descripcion"],
                          "Observaciones": prjfet["Observaciones"], "despesa": prjfet["Debe"],
                          "ingres": prjfet["Haber"]})
    resultado = json.dumps(resultado)
    return resultado

def AjaxListResumEstatCanonDatos(request,fecha_min,fecha_max,codigo):
    fecha_min = datetime.strptime(fecha_min, "%d-%m-%Y")
    fecha_max = datetime.strptime(fecha_max, "%d-%m-%Y")
    # fecha_min = projectes["data_min"]
    # fecha_max = projectes["data_max"]
    cursor = connections['contabilitat'].cursor()
    resultado = []
    proyectos = []
    nuevo_inv = 0  # es un chivato para indicar cuando empezamos a sumar los proyectos de otro investigador
    num_investigadores = 0
    #
    base_canon = 0
    percen_1 = 0
    canon_creaf = 0
    percen_2 = 0
    canon_oficial = 0
    dif_canon = 0
    ingressos = 0
    percen_3 = 0
    canon_aplicat = 0
    canon_pendent_aplicar = 0
    saldo_canon_oficial = 0
    #
    for proyecto in str(codigo).split(","):
        cod_responsable = proyecto.split("-")[0]
        id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
        cod_projecte = proyecto.split("-")[1]
        projecte = Projectes.objects.get(codi_prj=cod_projecte,
                                         id_resp=id_resp)  # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
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

        ### consulta SQL
        cursor.execute("SELECT ingressosD, ingressosH, canonD, canonH FROM "
                       "(SELECT CONVERT(varchar,Sum(DEBE))AS ingressosD, CONVERT(varchar,Sum(HABER))AS ingressosH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND CUENTAS.CUENTA LIKE '7%' AND CUENTAS.CUENTA NOT LIKE '79%' AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?))) AS ingressos,"
                       "(SELECT CONVERT(varchar,Sum(DEBE))AS canonD, CONVERT(varchar,Sum(HABER))AS canonH FROM __ASIENTOS INNER JOIN CUENTAS ON __ASIENTOS.IDCUENTA=CUENTAS.IDCUENTA WHERE (CENTROCOSTE2='   '+(?) AND (CUENTAS.CUENTA LIKE '79%' OR CUENTAS.CUENTA LIKE '6296%') AND TIPAPU='N'  AND CONVERT(date,FECHA,121)<=(?))) AS canon",
                       [codigo_entero, fecha_max, codigo_entero, fecha_max])
        projectfetch = dictfetchall(cursor)  # un cursor.description tambien sirve

        if projectfetch[0]["ingressosD"] is None:
            projectfetch[0]["ingressosD"] = 0
        if projectfetch[0]["ingressosH"] is None:
            projectfetch[0]["ingressosH"] = 0
        if projectfetch[0]["canonD"] is None:
            projectfetch[0]["canonD"] = 0
        if projectfetch[0]["canonH"] is None:
            projectfetch[0]["canonH"] = 0

        ingressosD = float(projectfetch[0]["ingressosD"])
        ingressosH = float(projectfetch[0]["ingressosH"])
        canonD = float(projectfetch[0]["canonD"])
        canonH = float(projectfetch[0]["canonH"])

        ###### CUENTAS

        ingressos = ingressosH - ingressosD
        canon_aplicat = canonD - canonH
        concedit = 0
        for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
            concedit = concedit + importe.import_concedit
        percen_iva = projecte.percen_iva
        canon_oficial = projecte.canon_oficial
        if concedit == 0:  # para evitar problemas con la division si es 0
            percen_canon_oficial = 0.00
        else:
            percen_canon_oficial = ((canon_oficial / concedit) * (100 * (1 + projecte.percen_iva / 100)))
        # Calculamos el canon mas grande entre el del creaf y el oficial,para luego calcular el canon total
        if percen_canon_oficial > projecte.percen_canon_creaf:
            canon_max = percen_canon_oficial
        else:
            canon_max = projecte.percen_canon_creaf

        iva = ((concedit * percen_iva) / (100 * (1 + percen_iva / 100)))
        base_canon = concedit  # Ojo que no es correct,o esto son los ingresos
        canon_creaf = (concedit * projecte.percen_canon_creaf) / (100 * (1 + projecte.percen_iva / 100))
        canon_total = (concedit - iva) * (canon_max / 100)
        # diferencia_per = (percen_canon_oficial-percen_canon_creaf)
        dif_canon = abs(
            canon_oficial - canon_creaf)  # Ojo la funcion abs() sirve para ver la diferencia entre 2 numeros, evitando asi un resultado con -
        if base_canon != 0:
            percen_1 = (canon_creaf / base_canon) * 100
            percen_2 = (canon_oficial / base_canon) * 100
        else:
            percen_1 = 0
            percen_2 = 0

        if ingressos != 0:
            percen_3 = (canon_aplicat / ingressos) * 100
        else:
            percen_3 = 0
        # net_disponible = concedit-iva-canon

        canon_pendent_aplicar = round(canon_creaf) - canon_aplicat
        saldo_canon_oficial = round(canon_oficial) - canon_aplicat
        # redondeamos para mostrar 2 decimales en los resultados

        base_canon = round(base_canon, 2)
        percen_1 = round(percen_1, 2)
        canon_creaf = round(canon_creaf, 2)
        percen_2 = round(percen_2, 2)
        canon_oficial = round(canon_oficial, 2)
        percen_canon_oficial = round(percen_canon_oficial, 4)
        dif_canon = round(dif_canon, 2)
        ingressos = round(ingressos, 2)
        percen_3 = round(percen_3, 2)
        canon_aplicat = round(canon_aplicat, 2)
        canon_pendent_aplicar = round(canon_pendent_aplicar, 2)
        saldo_canon_oficial = round(saldo_canon_oficial, 2)

        #############
        # Hora de ir sumando los resultados de cada proyecto del investigador
        proyectos.append({
            "codi": codigo_entero,
            "nom": projecte.acronim,
            "base_canon": base_canon,
            "percen_1": percen_1,
            "canon_creaf": canon_creaf,
            "percen_2": percen_2,
            "canon_oficial": canon_oficial,
            "percen_canon_oficial": percen_canon_oficial,
            "dif_canon": dif_canon,
            "ingressos": ingressos,
            "percen_3": percen_3,
            "canon_aplicat": canon_aplicat,
            "canon_pendent_aplicar": canon_pendent_aplicar,
            "saldo_canon_oficial": saldo_canon_oficial
        })

    resultado = json.dumps(proyectos)
    return resultado

def AjaxListJustificacionsCabecera(request,fecha_min,fecha_max):
    resultado=[]
    fecha_min = datetime.strptime(fecha_min, "%d-%m-%Y")
    fecha_max = datetime.strptime(fecha_max, "%d-%m-%Y")
    for justificacio in JustificProjecte.objects.filter(data_justificacio__gte=fecha_min, data_justificacio__lte=fecha_max):
        codigo_entero=str(justificacio.id_projecte.id_resp.codi_resp)+str("-")+str(justificacio.id_projecte.codi_prj)
        resultado.append({"data":str(justificacio.data_justificacio),"codi":codigo_entero,"nom":justificacio.id_projecte.acronim,"responsable":justificacio.id_projecte.id_resp.id_usuari.nom_usuari,"periode":"Del "+str(justificacio.data_inici_periode)+" al "+str(justificacio.data_fi_periode),"observacions":justificacio.comentaris})
    resultado = json.dumps(resultado)
    return resultado