from __builtin__ import int
from django.db import connections
from gestprj.models import Projectes,Responsables,Financadors, CentresParticipants, PersonalCreaf, PersonalExtern, Financadors, Receptors, Renovacions, Pressupost, PeriodicitatPartida, PeriodicitatPres,TConceptesPress, Desglossaments
from decimal import *


def dictfetchall(cursor):
    # Devuelve todos los campos de cada row como una lista
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def ContDades(projectes):#Fitxa Dades Projectes

        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)

            #####
            centres_participants = CentresParticipants.objects.filter(id_projecte= projecte.id_projecte)
            participants_creaf = PersonalCreaf.objects.filter(id_projecte=projecte.id_projecte)
            participants_externs = PersonalExtern.objects.filter(id_projecte=projecte.id_projecte)

            financadors = Financadors.objects.filter(id_projecte=projecte.id_projecte)
            receptors = Receptors.objects.filter(id_projecte=projecte.id_projecte)

        # CANON I IVA
            concedit=0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = round(concedit + float(importe.import_concedit),2)
            #vienen en la tabla:
            percen_iva = round(projecte.percen_iva,2)
            percen_canon_creaf = round(projecte.percen_canon_creaf,2)
            canon_oficial = round(projecte.canon_oficial,2)

            # calculados a mano
            if concedit == 0: # para evitar problemas con la division si es 0
                percen_canon_oficial = 0.00
            else:
                percen_canon_oficial = round(((canon_oficial / concedit)*(100*(1+percen_iva/100))),2)
            canon_creaf = round(((concedit*percen_canon_creaf)/(100*(1+percen_iva/100))),2)
            diferencia_per = round((percen_canon_oficial-percen_canon_creaf),2)
            diferencia_eur = round((canon_oficial - canon_creaf),2)
            iva = round((( concedit * percen_iva ) / (100*(1+percen_iva/100))),2)

            canoniva = {"percen_iva":percen_iva,"percen_canon_creaf":percen_canon_creaf,"canon_oficial":canon_oficial,"percen_canon_oficial":percen_canon_oficial,"canon_creaf":canon_creaf,"diferencia_per":diferencia_per,"diferencia_eur":diferencia_eur,"iva":iva}
        ####

        # DESPESES
            despeses = []
            despesa_total_concedit = 0
            despesa_total_iva = 0
            despesa_total_canon = 0
            despesa_total_net = 0
            for despesa in Renovacions.objects.filter(id_projecte=projecte.id_projecte):
                import_concedit = float(despesa.import_concedit)
                despesa_total_concedit = despesa_total_concedit+import_concedit
                iva = round((( import_concedit * percen_iva ) / 100),2)
                despesa_total_iva = despesa_total_iva+iva
                canon = round((( import_concedit * percen_canon_creaf ) / 100),2)
                despesa_total_canon = despesa_total_canon+canon
                net = round(( import_concedit - iva - canon ),2)
                despesa_total_net = despesa_total_net+net
                despeses.append({"data_inici":despesa.data_inici,"data_fi":despesa.data_fi,"concedit":import_concedit,"iva":iva,"canon":canon,"net":net})
                # concedit = round(concedit + float(importe.import_concedit),2)

        ####

        # PRESSUPOST
            partides = []
            max_periodes = 0;
            # al suma de cada periodo
            totals = [0,0,0,0,0,0,0,0]
            total_import = 0
            partida_total = 0

            # primero vemos cual es el max de periodos que tiene una de als partidas
            for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
                n_periodes = 0
                for periode in PeriodicitatPartida.objects.filter(id_partida=partida.id_partida):
                    n_periodes = n_periodes+1
                    if n_periodes > max_periodes:
                        max_periodes = n_periodes
            ######

            # Despues ponesmos los periodos en cada partida,usamos el max anterior para rellenar con 0 en caso de que haya menos periodos que el maximo
            for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
                periodes = []
                total_periode = 0

                for index,periode in enumerate(PeriodicitatPartida.objects.filter(id_partida=partida.id_partida)):
                    total_periode = total_periode+periode.import_field
                    totals[index] = totals[index]+periode.import_field
                    periodes.append({"importe":periode.import_field})

                if len(periodes) < max_periodes:
                    for dif in range((max_periodes-len(periodes))):
                        periodes.append({"importe":0.00})

                totals[max_periodes] = totals[max_periodes]+total_periode

            ######

                # Si no hay periodos,comprovar si las propias partidas tienen importe:
                if not periodes:
                    total_import = total_import+partida.import_field
                    partides.append({"concepte":partida.id_concepte_pres.desc_concepte,"import":partida.import_field})
                else:
                    partides.append({"concepte":partida.id_concepte_pres.desc_concepte,"periodes":periodes,"total":total_periode})

                ######
        ########


            # tam_periodes = round(max_periodes/8) #lo dividimos entre 8 para el boostrap,ya que quedan col-md-8 como tamano maximo(hay 2 divs que ocupan 2,el concepto y el total)
            resultado.append({"dades_prj":projecte,"codi_resp":cod_responsable,"codi_prj":cod_projecte,'centres_participants':centres_participants,'participants_creaf':participants_creaf,'participants_externs':participants_externs,'financadors':financadors,'receptors':receptors,'canoniva':canoniva,'despeses':despeses,'total_concedit':despesa_total_concedit,'total_iva':despesa_total_iva,'total_canon':despesa_total_canon,'total_net':despesa_total_net,'partides':partides,'totals_pres':totals,'max_periodes':range(max_periodes),'total_import_pres':total_import})

        return resultado

def ContEstatPres(projectes):# Estat Pressupostari Projectes


        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        proyectos = []
        periodos = []
        partidas = []
        for projecte_chk in projectes.getlist("prj_select"):
            #totales de totales
            total_prj_pressupostat=0
            total_prj_gastat = 0
            total_prj_saldo = 0
            tipos_partida = {}

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)

            #####
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit
            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva-canon

            concedit=round(concedit,2)
            iva=round(iva,2)
            canon=round(canon,2)
            net_disponible=round(net_disponible,2)
            #####

        # PRESSUPOST

            periodos = []
            n_periode = 0
            max_periodes = 0;
            # al suma de cada periodo
            totals = [0,0,0,0,0,0,0,0]
            total_import = 0
            partida_total = 0


            ######ZONA EXPERIMENTAL
            if PeriodicitatPres.objects.filter(id_projecte=projecte.id_projecte):#Si hay periodos
                for periode in PeriodicitatPres.objects.filter(id_projecte=projecte.id_projecte):
                    total_pressupostat = 0
                    total_gastat = 0
                    total_saldo =0
                    data_min_periode=str(periode.data_inicial)
                    data_max_periode=str(periode.data_final)
                    for partidaperio in PeriodicitatPartida.objects.filter(id_periodicitat=periode.id_periodicitat):#partida de x periodo
                        desc_partida=partidaperio.id_partida.id_concepte_pres.desc_concepte
                        #para el total de totales necesitaremos ir anadiendo aquellas partidas que no existan
                        if desc_partida not in tipos_partida:
                            tipos_partida[desc_partida]={"nom_partida":desc_partida,"total_pressupostat":0,"total_gastat":0,"total_saldo":0}
                        pressupostat=partidaperio.import_field

                        ### para obtener el gastat
                        gastat=0
                        for compte in Desglossaments.objects.filter(id_partida=partidaperio.id_partida):
                            cod_compte=str(compte.compte)
                            if cod_compte is None:
                                cod_compte="0000"
                            # primer_digito=str(cod_compte)[0] # solo son cuentas contables los que empiezan por 6 y 2
                            # if primer_digito =='6' or primer_digito =='2' :
                            if int(cod_compte)<1000:
                                if int(cod_compte)<100:
                                    if int(cod_compte)<10:
                                        cod_compte=cod_compte+"%%%"
                                    else:
                                        cod_compte=cod_compte+"%%"
                                else:
                                    cod_compte=cod_compte+"%"

                            codigo_final=cod_compte+codigo_entero#en realidad seria de 9 digitos pero como en la consulta ponemos un 6 o un delante es de 8
                            if compte.id_compte:
                                clau=str(compte.id_compte.clau_compte)
                                cursor.execute("SELECT Debe,Haber,Descripcion FROM Apuntes WHERE ( (Diario='0' OR Diario='4' OR Diario='1') AND ( Cuenta LIKE (?) AND Cuenta <>6296+(?) ) AND ( (Apuntes.Opc1=(?) AND Fecha<={d '2009-12-31'}) OR (Apuntes.Opc3=(?) AND Fecha>={d '2010-01-01'}) ) AND ( CONVERT(date,Fecha,105)<=(?) AND CONVERT(date,Fecha,105)>=(?) )  ) ",[codigo_final,codigo_entero,clau,clau,data_max_periode,data_min_periode])
                            else:
                                cursor.execute("SELECT Debe,Haber,Descripcion FROM Apuntes WHERE ( (Diario='0' OR Diario='4' OR Diario='1') AND ( Cuenta LIKE (?) AND Cuenta <>6296+(?) ) AND ( CONVERT(date,Fecha,105)<=(?) AND CONVERT(date,Fecha,105)>=(?) )  ) ",[codigo_final,codigo_entero,data_max_periode,data_min_periode])
                            cuentacont=dictfetchall(cursor) #Se puede usar un Sum(Debe) Sum(HAber) para ahorrarnos el bucle,pero de momento lo prefiero asi para comprobar los gastos uno a uno
                            if cuentacont:
                                for cont in cuentacont:
                                    if cont["Debe"] is None:
                                        cont["Debe"]=0
                                    if cont["Haber"] is None:
                                        cont["Haber"]=0
                                    gastat=gastat+(Decimal(cont["Debe"]-cont["Haber"]))
                        ####
                        saldo=pressupostat-gastat
                        #totales
                        total_pressupostat=total_pressupostat+pressupostat
                        total_gastat=total_gastat+gastat
                        total_saldo=total_saldo+saldo
                        #redondeo
                        pressupostat=round(pressupostat,2)
                        gastat=round(gastat,2)
                        saldo=round(saldo,2)
                        #los gastos de el tipo de partida con el que estamos actualmente se sumara al del proyecto
                        tipos_partida[desc_partida]["total_pressupostat"]=tipos_partida[desc_partida]["total_pressupostat"]+pressupostat
                        tipos_partida[desc_partida]["total_gastat"]=tipos_partida[desc_partida]["total_gastat"]+gastat
                        tipos_partida[desc_partida]["total_saldo"]=tipos_partida[desc_partida]["total_saldo"]+saldo
                        partidas.append({"descripcio":desc_partida,"pressupostat":pressupostat,"gastat":gastat,"saldo":saldo})
                    #redondeo totales
                    total_pressupostat=round(total_pressupostat,2)
                    total_gastat=round(total_gastat,2)
                    total_saldo=round(total_saldo,2)
                    #sumas a los totales del proyecto
                    total_prj_pressupostat=total_prj_pressupostat+total_pressupostat
                    total_prj_gastat=total_prj_gastat+total_gastat
                    total_prj_saldo=total_prj_saldo+saldo
                    #
                    periodos.append({"partides":partidas,"num_periode":n_periode,"total_pressupostat":total_pressupostat,"total_gastat":total_gastat,"total_saldo":total_saldo})
                    n_periode = n_periode+1
                    partidas = []

                resultado.append({"dades_prj":projecte,"periodes":periodos,"codi_resp":cod_responsable,"codi_prj":cod_projecte,"concedit":concedit,"canon":canon,"canon_percen":round(projecte.percen_canon_creaf,2),"iva":iva,"iva_percen":round(projecte.percen_iva,2),"net_disponible":net_disponible,"totales_partidas":tipos_partida,"total_prj_pressupostat":total_prj_pressupostat,"total_prj_gastat":total_prj_gastat,"total_prj_saldo":total_prj_saldo})
            else:#Si no hay periodos hay que comprobar igualmente los gastos
                for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):#partidas de proyecto
                        total_pressupostat = 0
                        total_gastat = 0
                        total_saldo =0
                        desc_partida=partida.id_concepte_pres.desc_concepte
                        #para el total de totales necesitaremos ir anadiendo aquellas partidas que no existan
                        if desc_partida not in tipos_partida:
                            tipos_partida[desc_partida]={"nom_partida":desc_partida,"total_pressupostat":0,"total_gastat":0,"total_saldo":0}
                        pressupostat=partida.import_field

                        ### para obtener el gastat
                        gastat=0
                        for compte in Desglossaments.objects.filter(id_partida=partida.id_partida):
                            cod_compte=str(compte.compte)
                            if cod_compte is None:
                                cod_compte="0000"
                            # primer_digito=str(cod_compte)[0] # solo son cuentas contables los que empiezan por 6 y 2
                            # if primer_digito =='6' or primer_digito =='2' :
                            if int(cod_compte)<1000:
                                if int(cod_compte)<100:
                                    if int(cod_compte)<10:
                                        cod_compte=cod_compte+"%%%"
                                    else:
                                        cod_compte=cod_compte+"%%"
                                else:
                                    cod_compte=cod_compte+"%"

                            codigo_final=cod_compte+codigo_entero#en realidad seria de 9 digitos pero como en la consulta ponemos un 6 o un delante es de 8
                            cursor.execute("SELECT Debe,Haber,Descripcion FROM Apuntes WHERE ( (Diario='0' OR Diario='4' OR Diario='1') AND ( Cuenta LIKE (?) AND Cuenta <>6296+(?) ) ) ",[codigo_final,codigo_entero])
                            cuentacont=dictfetchall(cursor)
                            if cuentacont:
                                for cont in cuentacont:
                                    if cont["Debe"] is None:
                                        cont["Debe"]=0
                                    if cont["Haber"] is None:
                                        cont["Haber"]=0
                                    gastat=gastat+(Decimal(cont["Debe"]-cont["Haber"]))
                        ####
                        saldo=pressupostat-gastat
                        #totales
                        total_pressupostat=total_pressupostat+pressupostat
                        total_gastat=total_gastat+gastat
                        total_saldo=total_saldo+saldo
                        #redondeo
                        pressupostat=round(pressupostat,2)
                        gastat=round(gastat,2)
                        saldo=round(saldo,2)
                        #sumas a los totales del proyecto
                        total_prj_pressupostat=total_prj_pressupostat+total_pressupostat
                        total_prj_gastat=total_prj_gastat+total_gastat
                        total_prj_saldo=total_prj_saldo+saldo
                        #los gastos de el tipo de partida con el que estamos actualmente se sumara al del proyecto
                        tipos_partida[desc_partida]["total_pressupostat"]=tipos_partida[desc_partida]["total_pressupostat"]+pressupostat
                        tipos_partida[desc_partida]["total_gastat"]=tipos_partida[desc_partida]["total_gastat"]+gastat
                        tipos_partida[desc_partida]["total_saldo"]=tipos_partida[desc_partida]["total_saldo"]+saldo
                        partidas.append({"descripcio":desc_partida,"pressupostat":pressupostat,"gastat":gastat,"saldo":saldo})
                resultado.append({"dades_prj":projecte,"codi_resp":cod_responsable,"codi_prj":cod_projecte,"concedit":concedit,"canon":canon,"canon_percen":round(projecte.percen_canon_creaf,2),"iva":iva,"iva_percen":round(projecte.percen_iva,2),"net_disponible":net_disponible,"totales_partidas":tipos_partida,"total_prj_pressupostat":total_prj_pressupostat,"total_prj_gastat":total_prj_gastat,"total_prj_saldo":total_prj_saldo})

        return resultado



def ContDespeses(projectes):#Seguiment Despeses Projectes
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj

            ##### poner 0 en los codigos si son demasiado cortos para tener x tamano
            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)
            #####
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit
            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva-canon

            concedit = round(concedit,2)
            iva = round(iva,2)
            canon = round(canon,2)
            net_disponible = round(net_disponible,2)
            #####

            # 105 en el convert equivale al dd-mm-yyyy
            cursor.execute("SELECT TOP 100 PERCENT CONVERT(VARCHAR,Fecha,105)as Data, Asiento, Documento, Cuenta, Opc1, Opc3, Descripcion, Opc2, Debe, Haber FROM  Apuntes WHERE ((Diario='0' OR Diario='1' OR Diario='4') AND (((Cuenta LIKE '2%'+(?)) OR (Cuenta LIKE '6%'+(?))) AND (Cuenta <> '6296'+(?))) AND ((Fecha >= CONVERT(date,(?),105)) AND (Fecha<=CONVERT(date,(?),105)))) ORDER BY cast(Fecha as date)",[codigo_entero,codigo_entero,codigo_entero,fecha_min,fecha_max])
            projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve

            ##### Para ir restando el saldo a medida que salen gastos:
            saldo_disponible = float(net_disponible)
            total_despeses = 0
            for prjfet in projectfetch:
                if prjfet["Debe"] == None:
                    prjfet["Debe"] = 0
                else:
                    saldo_disponible = saldo_disponible - prjfet["Debe"]
                    total_despeses = total_despeses+prjfet["Debe"]

                if saldo_disponible<0.1 and saldo_disponible>-0.1: # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
                    saldo_disponible = 0

                prjfet["saldo_disponible"] = saldo_disponible

            #####
            total_disponible = saldo_disponible

            resultado.append({"dades_prj":projecte,"despeses":projectfetch,"concedit":concedit,"iva_percen":float(projecte.percen_iva),"iva":iva,"canon_percen":float(projecte.percen_canon_creaf),"canon":canon,"net_disponible":net_disponible,"total_despeses":total_despeses,"total_disponible":total_disponible,'data_min':fecha_min,'data_max':fecha_max,"codi_resp":cod_responsable,"codi_prj":cod_projecte})

        return resultado


def ContIngresos(projectes):#Seguiment Ingressos Projectes
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            ##### poner 0 en los codigos si son demasiado cortos para tener x tamano

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)
            #####
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit
            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva
            #####

            # 105 en el convert equivale al dd-mm-yyyy
            cursor.execute("SELECT TOP 100 PERCENT CONVERT(VARCHAR,Fecha,105)as Data, Asiento, Cuenta, Descripcion, Debe, Haber FROM  Apuntes WHERE ((Diario='0' OR Diario='1' OR Diario='4') AND (Cuenta LIKE '7%'+(?)) AND (Cuenta <> '6296'+(?)) AND ((Fecha >= CONVERT(date,(?),105)) AND (Fecha<=CONVERT(date,(?),105)))) ORDER BY cast(Fecha as date)",[codigo_entero,codigo_entero,fecha_min,fecha_max])
            projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve

            ##### Para ir restando el saldo pendiente a medida que salen ingresos:
            saldo_pendiente = float(net_disponible)
            total_ingresos = 0
            for prjfet in projectfetch:
                if prjfet["Haber"] == None:
                    prjfet["Haber"] = 0
                else:
                    saldo_pendiente = saldo_pendiente - prjfet["Haber"]
                    total_ingresos = total_ingresos+prjfet["Haber"]

                if saldo_pendiente<0.1 and saldo_pendiente>-0.1: # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
                    saldo_pendiente = 0
                prjfet["saldo_pendiente"] = saldo_pendiente

            #####
            total_pendiente = saldo_pendiente

            resultado.append({"dades_prj":projecte,"ingresos":projectfetch,"concedit":concedit,"iva_percen":float(projecte.percen_iva),"iva":iva,"net_disponible":net_disponible,"total_pendiente":total_pendiente,"total_ingresos":total_ingresos,'data_min':fecha_min,'data_max':fecha_max,"codi_resp":cod_responsable,"codi_prj":cod_projecte})

        return resultado

def FitxaMajorProjectes(projectes):#Fitxa Major Projectes (Ingressos i Despeses)
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            ##### poner 0 en los codigos si son demasiado cortos para tener x tamano

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)
            #####
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit
            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva-canon

            concedit = round(concedit,2)
            iva = round(iva,2)
            canon = round(canon,2)
            net_disponible = round(net_disponible,2)
            ##### OJO que para ir restando el saldo hay que devolver los resultados ordenados por la fecha,para ello he tenido que modificar el ORDER BY
            cursor.execute("SELECT TOP 100 PERCENT CONVERT(VARCHAR,Fecha,105) as Fecha, Asiento, Cuenta, Descripcion, Debe, Haber FROM  Apuntes WHERE ((Diario='0' OR Diario='1' OR Diario='4') AND ((Cuenta LIKE '2%'+(?)) OR (Cuenta LIKE '6%'+(?)) OR (Cuenta LIKE '7%'+(?))) AND ((Fecha >=CONVERT(date, (?),105)) AND (Fecha<=CONVERT(date, (?),105)))) ORDER BY cast(Fecha as date)",[codigo_entero,codigo_entero,codigo_entero,fecha_min,fecha_max])
            projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve


            ##### Para ir restando el saldo a medida que salen gastos:
            total_caja = 0 # ES EL SALDO INICIAL ****SIEMPRE ES 0???????
            total_debe = 0
            total_haber = 0
            for prjfet in projectfetch:
                if prjfet["Debe"] == None:
                    prjfet["Debe"] = 0
                if prjfet["Haber"] == None:
                    prjfet["Haber"] = 0

                prjfet["Saldo_caja"] = round(total_caja+(prjfet["Haber"]-prjfet["Debe"]),2)
                total_debe = total_debe+prjfet["Debe"]
                total_haber = total_haber+prjfet["Haber"]
                total_caja = prjfet["Saldo_caja"]


                if total_caja<0.1 and total_caja>-0.1: # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
                    total_disponible = 0

                if total_debe<0.1 and total_debe>-0.1:
                    total_debe = 0

                if total_haber<0.1 and total_haber>-0.1:
                    total_haber = 0



            #####
            total_caja = round(total_caja,2)
            total_debe = round(total_debe,2)
            total_haber = round(total_haber,2)
            #####
            resultado.append({"dades_prj":projecte,"despeses":projectfetch,"concedit":concedit,"iva_percen":round(float(projecte.percen_iva),2),"iva":iva,"canon_percen":round(float(projecte.percen_canon_creaf),2),"canon":canon,"net_disponible":net_disponible,"total_caja":total_caja,"total_debe":total_debe,"total_haber":total_haber,'data_min':fecha_min,'data_max':fecha_max,"codi_resp":cod_responsable,"codi_prj":cod_projecte})

        return resultado

def EstatProjectesResp(projectes):#Estat Projectes per Responsable
    ## Este es muy similar al de ResumEstatProjectes,pero habra que mostrar los datos proyecto a proyecto y ordenados por responsable
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []#este contendra varios "datos_inv"cada uno representa a un investigador
        datos_inv = []#este contendra 2 arrays,uno con todos los proyectos del investigador y sus datos ("projecte") y otro con los "totals"s
        investigadores = {} #diccionario
        proyectos = []
        nuevo_inv = 0 #es un chivato para indicar cuando empezamos a sumar los proyectos de otro investigador
        num_investigadores = 0

        # totales para el footer
        totals = []
        total_concedit = 0
        total_iva = 0
        total_canon_total = 0
        total_ingressos = 0
        total_pendent = 0
        total_despeses = 0
        total_canon_aplicat = 0
        total_disponible_caixa = 0
        total_disponible_real = 0

        # Averiguar el numero de investigadores a partir de inspeccionar todos los proyectos que hemos recibido
        for projecte_chk in projectes.getlist("prj_select"):
            cod_responsable = projecte_chk.split("-")[0]
            if int(cod_responsable) not in investigadores:
                investigadores[int(cod_responsable)]=int(cod_responsable)
                num_investigadores=num_investigadores+1

        #Ahora empieza lo bueno
        for inv in investigadores:
            nuevo_inv = 1
            iva=0
            canon_max = 0
            nom_resp = Responsables.objects.get(codi_resp=inv).id_usuari.nom_usuari
            for projecte_chk in projectes.getlist("prj_select"):
                cod_responsable = projecte_chk.split("-")[0]

                if(inv==int(cod_responsable)):
                    ##### Para extraer el objeto proyecto y el codigo:
                    id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
                    cod_projecte = projecte_chk.split("-")[1]
                    projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
                    ##### poner 0 en los codigos si son demasiado cortos para tener x tamano
                    if int(cod_responsable) < 10:
                        cod_responsable="0"+str(cod_responsable)
                    if int(cod_projecte) < 100:
                        if int(cod_projecte) < 10:
                            cod_projecte="00"+str(cod_projecte)
                        else:
                            cod_projecte="0"+str(cod_projecte)
                    #####
                    codigo_entero=cod_responsable+cod_projecte
                    #####

                    ##### Cuentas:
                    concedit=0
                    for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                        concedit = concedit + importe.import_concedit

                    iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
                    canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
                    net_disponible = concedit-iva-canon

                    #Calculamos el canon mas grande entre el del creaf y el oficial,para luego calcular el canon total

                    if concedit == 0: # para evitar problemas con la division si es 0
                        percen_canon_oficial = 0.00
                    else:
                        percen_canon_oficial = ((projecte.canon_oficial / concedit)*(100*(1+projecte.percen_iva/100)))

                    if percen_canon_oficial > projecte.percen_canon_creaf:
                        canon_max = percen_canon_oficial
                    else:
                        canon_max = projecte.percen_canon_creaf

                    canon_total = round((concedit-iva) * (canon_max/100))
                    concedit = round(concedit,2)
                    iva = round(iva,2)
                    canon = round(canon,2)
                    net_disponible = round(net_disponible,2)

                    #############
                    ### consulta SQL

                    cursor.execute("SELECT ingressosD, ingressosH, despesesD, despesesH, canonD, canonH FROM ( SELECT Sum(Debe) AS ingressosD, Sum(Haber) AS ingressosH FROM Apuntes WHERE(Diario='0' OR Diario='4' OR Diario='1') AND (Cuenta LIKE '7%'+(?) AND Cuenta<>'7900'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as ingressos, ( SELECT Sum(Debe) AS despesesD, Sum(Haber) AS despesesH FROM Apuntes WHERE (Diario='0' OR Diario='4' OR Diario='1') AND ((Cuenta LIKE'6%'+(?) OR Cuenta LIKE'2%'+(?)) AND Cuenta<>'6296'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as despeses, ( SELECT Sum(Debe) AS canonD, Sum(Haber) AS canonH FROM Apuntes WHERE (Diario='0' OR Diario='4' OR Diario='1') AND (Cuenta='7900'+(?) OR Cuenta='6296'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as canon",[codigo_entero,codigo_entero,fecha_max,codigo_entero,codigo_entero,codigo_entero,fecha_max,codigo_entero,codigo_entero,fecha_max])
                    projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve

                    ingressosD=projectfetch[0]["ingressosD"]
                    ingressosH=projectfetch[0]["ingressosH"]
                    despesesD=projectfetch[0]["despesesD"]
                    despesesH=projectfetch[0]["despesesH"]
                    canonD=projectfetch[0]["canonD"]
                    canonH=projectfetch[0]["canonH"]

                    if ingressosD is None :
                        ingressosD=0
                    if ingressosH is None :
                        ingressosH=0
                    if despesesD is None :
                        despesesD=0
                    if despesesH is None :
                        despesesH=0
                    if canonD is None :
                        canonD=0
                    if canonH is None :
                        canonH=0

                    #Calculamos algunos campos a partir de lo obtenido de contabilidad
                    ingressos = round(ingressosH-ingressosD,2)
                    despeses= round(despesesD-despesesH,2)# OJO! que los que en los que estan tancats las despesas suelen coincir con el net_disponible,pero siempre es despesesD-H
                    canon_aplicat =round(canonD-canonH,2)
                    disponible_caixa = round(ingressos-despeses-canon_aplicat,2)
                    disponible_real = round(concedit-iva-canon_total-despeses,2)# OJO esta ok,solo que como algunos importes salen x100 tiene un valor elevado.
                    pendent = round(abs(disponible_caixa-disponible_real),2)
                    #
                    # Hora de ir sumando los resultados de cada proyecto del investigador
                    proyectos.append({
                        "codi":codigo_entero,
                        "nom":projecte.acronim,
                        "concedit":concedit,
                        "iva":iva,
                        "canon_total":canon_total,
                        "despeses":despeses,
                        "pendent":pendent,
                        "ingressos":ingressos,
                        "canon_aplicat":canon_aplicat,
                        "disponible_caixa":disponible_caixa,
                        "disponible_real":disponible_real
                    })

                    #totales:
                    total_concedit = round(total_concedit+concedit,2)
                    total_iva = round(total_iva+iva,2)
                    total_canon_total = round(total_canon_total+canon_total,2)
                    total_ingressos = round(total_ingressos+ingressos,2)
                    total_pendent = round(total_pendent+total_pendent,2)
                    total_despeses = round(total_despeses+despeses,2)
                    total_canon_aplicat = round(total_canon_aplicat+canon_aplicat,2)
                    total_disponible_caixa = round(total_disponible_caixa+disponible_caixa,2)
                    total_disponible_real = round(total_disponible_real+disponible_real,2)


                    #

            #anadimos finalmente los totales al investigador,y este,al resultado
            totals.append({"total_concedit":total_concedit,"total_iva":total_iva,"total_canon_total":total_canon_total,"total_ingressos":total_ingressos,"total_pendent":total_pendent,"total_despeses":total_despeses,"total_canon_aplicat":total_canon_aplicat,"total_disponible_caixa":total_disponible_caixa,"total_disponible_real":total_disponible_real})
            datos_inv.append({"nom_responsable":nom_resp,"data_max":fecha_max,"projectes":proyectos,"totals":totals})
            resultado.append(datos_inv)
            proyectos = []
            totals = []
            datos_inv = []


        return resultado

def ResumFitxaMajorProjectes(projectes):#Resum Fitxa Major Projectes per Comptes
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        comptes =  {} #diccionario
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            ### poner 0 en los codigos si son demasiado cortos para tener x tamano

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)
            ###
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit=0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit

            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva-canon
            #####

            #obtener las cuentas de x proyecto
            cursor.execute("SELECT TOP 100 PERCENT Apuntes.Cuenta, Plan_cuentas.Titulo, Sum(Apuntes.Debe) AS TotalDebe, Sum(Apuntes.Haber) AS TotalHaber FROM Plan_cuentas LEFT JOIN Apuntes ON (Plan_cuentas.Cuenta = Apuntes.Cuenta) WHERE ( (Plan_cuentas.Nivel=0) AND (((Apuntes.Cuenta) LIKE '2%'+(?))OR((Apuntes.Cuenta) LIKE '6%'+(?) )OR((Apuntes.Cuenta) LIKE '7%'+(?))) AND ((Apuntes.Diario)='0' OR (Apuntes.Diario)='4' OR (Apuntes.Diario)='1') AND ((Apuntes.Fecha)>=CONVERT(date, (?),105) AND (Apuntes.Fecha)<=CONVERT(date, (?),105))) GROUP BY Apuntes.Cuenta, Plan_cuentas.Titulo ORDER BY Apuntes.Cuenta",[codigo_entero,codigo_entero,codigo_entero,fecha_min,fecha_max])
            projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve

            ##### Para ir restando el saldo a medida que salen gastos:
            total_disponible = 0 # ES EL SALDO INICIAL ****SIEMPRE ES 0???????
            total_debe = 0
            total_haber = 0
            for prjfet in projectfetch:
                if prjfet["TotalDebe"] == None:
                    prjfet["TotalDebe"] = 0
                if prjfet["TotalHaber"] == None:
                    prjfet["TotalHaber"] = 0
                #por cada cuenta,guardar los detalles/movimientos de la misma
                cursor.execute("SELECT TOP 100 PERCENT Fecha, Asiento, Cuenta, Descripcion, Debe, Haber FROM Apuntes WHERE (Cuenta=(?) AND (Diario='0' OR Diario='4' OR Diario='1') AND ((Apuntes.Fecha)>=CONVERT(date, (?),105) AND (Apuntes.Fecha)<=CONVERT(date, (?),105))) ORDER BY cast(Fecha as date)",[prjfet["Cuenta"],fecha_min,fecha_max])
                comptes[prjfet["Cuenta"]]=dictfetchall(cursor)


                total_debe = total_debe+prjfet["TotalDebe"]
                total_haber = total_haber+prjfet["TotalHaber"]
                total_disponible = round(total_disponible - prjfet["TotalDebe"] + prjfet["TotalHaber"],2)


                if total_disponible<0.1 and total_disponible>-0.1: # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
                    total_disponible = 0

                if total_debe<0.1 and total_debe>-0.1:
                    total_debe = 0

                if total_haber<0.1 and total_haber>-0.1:
                    total_haber = 0

                prjfet["Total_disponible"] = total_disponible

            #####
            concedit = round(concedit,2)
            iva = round(iva,2)
            canon = round
            total_disponible = round(total_disponible,2)
            total_debe = round(total_debe,2)
            total_haber = round(total_haber,2)
            #####
            resultado.append({"dades_prj":projecte,"despeses":projectfetch,"comptes":comptes,"concedit":concedit,"iva_percen":round(float(projecte.percen_iva),2),"iva":iva,"canon_percen":round(float(projecte.percen_canon_creaf),2),"canon":canon,"net_disponible":net_disponible,"total_disponible":total_disponible,"total_debe":total_debe,"total_haber":total_haber,'data_min':fecha_min,'data_max':fecha_max,"codi_resp":cod_responsable,"codi_prj":cod_projecte})

        return resultado

#OJO que este esta relacionado con resum fitxa projecte
def MovimentsCompte(compte,data_min,data_max):
    if compte is None:
        return None
    else:
        fecha_min = data_min
        fecha_max = data_max
        cursor = connections['contabilitat'].cursor()
        #he modificado el primer resultado y ultimo resultado(que eran simplemente "Fecha"),el primero para que devuelva un "Fecha" como string en lugar de en partes,y el ultimo para relizar los calculos del saldo(ya que se deben hacer de mas antiguos a nuevos)
        cursor.execute("SELECT TOP 100 PERCENT CONVERT(date, Fecha,105) AS Fecha, Asiento, Cuenta, Descripcion, Debe, Haber FROM Apuntes WHERE (Cuenta=(?) AND (Diario='0' OR Diario='4' OR Diario='1') AND ((Apuntes.Fecha)>=CONVERT(date, (?),105) AND (Apuntes.Fecha)<=CONVERT(date, (?),105))) ORDER BY cast(Fecha as date)",[compte,fecha_min,fecha_max])
        fetch =  dictfetchall(cursor)
        saldo = 0
        for result in fetch:
            if result['Debe'] is None:
                result['Debe'] = 0
            if result['Haber'] is None:
                result['Haber'] = 0

            saldo = round((saldo-result["Debe"])+result["Haber"],2)
            result["Saldo"]=saldo
        return fetch

def ResumEstatProjectes(projectes):#Resum Estat Projectes

    ## En este caso devolveremos 2 arrays,uno con los datos y otro con los totales (mirar el return para mas info)
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        investigadores = {} #diccionario
        proyectos = []
        nuevo_inv = 0 #es un chivato para indicar cuando empezamos a sumar los proyectos de otro investigador
        num_investigadores = 0

        # totales para el footer
        totals = []
        total_concedit = 0
        total_iva = 0
        total_canon_total = 0
        total_ingressos = 0
        total_pendent = 0
        total_despeses = 0
        total_canon_aplicat = 0
        total_disponible_caixa = 0
        total_disponible_real = 0

        # Averiguar el numero de investigadores a partir de inspeccionar todos los proyectos que hemos recibido
        for projecte_chk in projectes.getlist("prj_select"):
            cod_responsable = projecte_chk.split("-")[0]
            if int(cod_responsable) not in investigadores:
                investigadores[int(cod_responsable)]=int(cod_responsable)
                num_investigadores=num_investigadores+1

        #Ahora empieza lo bueno
        for inv in investigadores:
            nuevo_inv = 1
            iva=0
            canon_max = 0
            for projecte_chk in projectes.getlist("prj_select"):
                cod_responsable = projecte_chk.split("-")[0]

                if(inv==int(cod_responsable)):
                    ##### Para extraer el objeto proyecto y el codigo:
                    id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
                    cod_projecte = projecte_chk.split("-")[1]
                    projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
                    ##### poner 0 en los codigos si son demasiado cortos para tener x tamano
                    if int(cod_responsable) < 10:
                        cod_responsable="0"+str(cod_responsable)
                    if int(cod_projecte) < 100:
                        if int(cod_projecte) < 10:
                            cod_projecte="00"+str(cod_projecte)
                        else:
                            cod_projecte="0"+str(cod_projecte)
                    #####
                    codigo_entero=cod_responsable+cod_projecte
                    #####

                    ##### Cuentas:
                    concedit=0
                    for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                        concedit = concedit + importe.import_concedit

                    iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
                    canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
                    net_disponible = concedit-iva-canon

                    #Calculamos el canon mas grande entre el del creaf y el oficial,para luego calcular el canon total

                    if concedit == 0: # para evitar problemas con la division si es 0
                        percen_canon_oficial = 0.00
                    else:
                        percen_canon_oficial = ((projecte.canon_oficial / concedit)*(100*(1+projecte.percen_iva/100)))

                    if percen_canon_oficial > projecte.percen_canon_creaf:
                        canon_max = percen_canon_oficial
                    else:
                        canon_max = projecte.percen_canon_creaf

                    canon_total = round((concedit-iva) * (canon_max/100))
                    concedit = round(concedit,2)
                    iva = round(iva,2)
                    canon = round(canon,2)
                    net_disponible = round(net_disponible,2)

                    #############
                    ### consulta SQL

                    cursor.execute("SELECT ingressosD, ingressosH, despesesD, despesesH, canonD, canonH FROM ( SELECT Sum(Debe) AS ingressosD, Sum(Haber) AS ingressosH FROM Apuntes WHERE(Diario='0' OR Diario='4' OR Diario='1') AND (Cuenta LIKE '7%'+(?) AND Cuenta<>'7900'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as ingressos, ( SELECT Sum(Debe) AS despesesD, Sum(Haber) AS despesesH FROM Apuntes WHERE (Diario='0' OR Diario='4' OR Diario='1') AND ((Cuenta LIKE'6%'+(?) OR Cuenta LIKE'2%'+(?)) AND Cuenta<>'6296'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as despeses, ( SELECT Sum(Debe) AS canonD, Sum(Haber) AS canonH FROM Apuntes WHERE (Diario='0' OR Diario='4' OR Diario='1') AND (Cuenta='7900'+(?) OR Cuenta='6296'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as canon",[codigo_entero,codigo_entero,fecha_max,codigo_entero,codigo_entero,codigo_entero,fecha_max,codigo_entero,codigo_entero,fecha_max])
                    projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve


                    if nuevo_inv == 1:
                        nuevo_inv = 0
                        #comprobar que no haya nones con el primer fetch
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

                        proyectos.append(projectfetch)

                        proyectos[0][0]["iva"] = iva
                        proyectos[0][0]["canon_total"] = canon_total
                        proyectos[0][0]["concedit"] = concedit
                        proyectos[0][0]["despeses"] = net_disponible
                        proyectos[0][0]["pendent"] = 0 # Ojo averiguar de donde sacar este valor

                    else:
                        #pese a la comprobacion anterior,nos hara falta quitar los none por cada proyecto
                        ingressosD=projectfetch[0]["ingressosD"]
                        ingressosH=projectfetch[0]["ingressosH"]
                        despesesD=projectfetch[0]["despesesD"]
                        despesesH=projectfetch[0]["despesesH"]
                        canonD=projectfetch[0]["canonD"]
                        canonH=projectfetch[0]["canonH"]

                        if ingressosD is None :
                            ingressosD=0
                        if ingressosH is None :
                            ingressosH=0
                        if despesesD is None :
                            despesesD=0
                        if despesesH is None :
                            despesesH=0
                        if canonD is None :
                            canonD=0
                        if canonH is None :
                            canonH=0
                        #Hora de ir sumando los resultados de cada proyecto del investigador
                        proyectos[0][0]["ingressosD"]=round(proyectos[0][0]["ingressosD"])+round(ingressosD)
                        proyectos[0][0]["ingressosH"]=round(proyectos[0][0]["ingressosH"])+round(ingressosH)
                        proyectos[0][0]["despesesD"]=round(proyectos[0][0]["despesesD"])+round(despesesD)
                        proyectos[0][0]["despesesH"]=round(proyectos[0][0]["despesesH"])+round(despesesH)
                        proyectos[0][0]["canonD"]=round(proyectos[0][0]["canonD"])+round(canonD)
                        proyectos[0][0]["canonH"]=round(proyectos[0][0]["canonH"])+round(canonH)

                        proyectos[0][0]["concedit"]=round(proyectos[0][0]["concedit"]+concedit,2) # proyectos[0][0]["concedit"]=round(proyectos[0][0]["ingressos"]+proyectos[0][0]["iva"])
                        proyectos[0][0]["iva"]=round(proyectos[0][0]["iva"]+iva,2)
                        proyectos[0][0]["canon_total"]=round(proyectos[0][0]["canon_total"]+canon_total,2)
                        proyectos[0][0]["despeses"]=round(proyectos[0][0]["despeses"]+net_disponible,2) # OJO! que deberia ser asi proyectos[0][0]["despeses"]=round(proyectos[0][0]["despesesD"]-proyectos[0][0]["despesesH"]) y quitar los demas proyectos[0][0][despeses]


                    #Estas variables son una suma de la de los proyectos del investigador
                    proyectos[0][0]["cod_responsable"]=cod_responsable # este y el de abajo so correctos pero se superponen una y otra vez por cada proyecto,a ver si se puede mejorar
                    proyectos[0][0]["nom_responsable"]=Responsables.objects.get(codi_resp=cod_responsable).id_usuari.nom_usuari

                    proyectos[0][0]["ingressos"]=round(proyectos[0][0]["ingressosH"]-proyectos[0][0]["ingressosD"],2)
                    proyectos[0][0]["canon_aplicat"]=round(proyectos[0][0]["canonD"]-proyectos[0][0]["canonH"])
                    proyectos[0][0]["disponible_caixa"]=round(proyectos[0][0]["ingressos"]-proyectos[0][0]["despeses"]-proyectos[0][0]["canon_aplicat"])
                    proyectos[0][0]["disponible_real"]=round(proyectos[0][0]["concedit"]-proyectos[0][0]["iva"]-proyectos[0][0]["canon_total"]-proyectos[0][0]["despeses"])
                    #totales:
                    total_concedit = round(total_concedit+proyectos[0][0]["concedit"],2)
                    total_iva = round(total_iva+proyectos[0][0]["iva"],2)
                    total_canon_total = round(total_canon_total+proyectos[0][0]["canon_total"],2)
                    total_ingressos = round(total_ingressos+proyectos[0][0]["ingressos"],2)
                    total_pendent = round(total_pendent+proyectos[0][0]["pendent"],2)
                    total_despeses = round(total_despeses+proyectos[0][0]["despeses"],2)
                    total_canon_aplicat = round(total_canon_aplicat+proyectos[0][0]["canon_aplicat"],2)
                    total_disponible_caixa = round(total_disponible_caixa+proyectos[0][0]["disponible_caixa"],2)
                    total_disponible_real = round(total_disponible_real+proyectos[0][0]["disponible_real"],2)
                    #
            resultado.append(proyectos)

            proyectos= []

        #anadimos finalmente solo los totales
        totals.append({"total_concedit":total_concedit,"total_iva":total_iva,"total_canon_total":total_canon_total,"total_ingressos":total_ingressos,"total_pendent":total_pendent,"total_despeses":total_despeses,"total_canon_aplicat":total_canon_aplicat,"total_disponible_caixa":total_disponible_caixa,"total_disponible_real":total_disponible_real})
        return resultado,totals



def ResumEstatCanon(projectes):#Resum Estat Canon Projectes per Responsable
    fecha_min = projectes["data_min"]
    fecha_max = projectes["data_max"]
    cursor = connections['contabilitat'].cursor()
    resultado = []
    datos_inv = []#este contendra 2 arrays,uno con todos los proyectos del investigador y sus datos ("projecte") y otro con los "totals"s
    investigadores = {} #diccionario
    proyectos = []
    nuevo_inv = 0 #es un chivato para indicar cuando empezamos a sumar los proyectos de otro investigador
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
    # totales para el footer
    totals = []
    total_base_canon = 0
    total_percen_1 = 0
    total_canon_creaf = 0
    total_percen_2 = 0
    total_canon_oficial = 0
    total_dif_canon = 0
    total_ingressos = 0
    total_percen_3 = 0
    total_canon_aplicat = 0
    total_canon_pendent_aplicar = 0
    total_saldo_canon_oficial = 0

    # Averiguar el numero de investigadores a partir de inspeccionar todos los proyectos que hemos recibido
    for projecte_chk in projectes.getlist("prj_select"):
        cod_responsable = projecte_chk.split("-")[0]
        if int(cod_responsable) not in investigadores:
            investigadores[int(cod_responsable)]=int(cod_responsable)
            num_investigadores=num_investigadores+1

    #Ahora empieza lo bueno
    for inv in investigadores:
        nuevo_inv = 1
        canon_max = 0
        nom_resp = Responsables.objects.get(codi_resp=inv).id_usuari.nom_usuari
        for projecte_chk in projectes.getlist("prj_select"):
            cod_responsable = projecte_chk.split("-")[0]

            if(inv==int(cod_responsable)):
                ##### Para extraer el objeto proyecto y el codigo:
                id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
                cod_projecte = projecte_chk.split("-")[1]
                projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
                ##### poner 0 en los codigos si son demasiado cortos para tener x tamano
                if int(cod_responsable) < 10:
                    cod_responsable="0"+str(cod_responsable)
                if int(cod_projecte) < 100:
                    if int(cod_projecte) < 10:
                        cod_projecte="00"+str(cod_projecte)
                    else:
                        cod_projecte="0"+str(cod_projecte)
                #####
                codigo_entero=cod_responsable+cod_projecte
                #####

                ### consulta SQL
                cursor.execute("SELECT ingressosD, ingressosH, canonD, canonH FROM ( SELECT Sum(Debe) AS ingressosD, Sum(Haber) AS ingressosH FROM Apuntes WHERE (Diario='0' OR Diario='4' OR Diario='1') AND Cuenta LIKE'7%'+(?) AND Cuenta<>'7900'+(?) AND (Fecha<= CONVERT(date, (?),105))) as ingressos, ( SELECT Sum(Debe) AS canonD, Sum(Haber) AS canonH FROM Apuntes WHERE (Diario='0' OR Diario='4' OR Diario='1') AND (Cuenta='7900'+(?) OR Cuenta='6296'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as canon",[codigo_entero,codigo_entero,fecha_max,codigo_entero,codigo_entero,fecha_max])
                projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve

                ingressosD=projectfetch[0]["ingressosD"]
                ingressosH=projectfetch[0]["ingressosH"]
                canonD=projectfetch[0]["canonD"]
                canonH=projectfetch[0]["canonH"]

                if ingressosD is None :
                    ingressosD=0
                if ingressosH is None :
                    ingressosH=0
                if canonD is None :
                    canonD=0
                if canonH is None :
                    canonH=0



                ###### CUENTAS

                ingressos = ingressosH-ingressosD
                canon_aplicat = canonD-canonH
                concedit=0
                for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                    concedit = concedit + importe.import_concedit
                percen_iva = projecte.percen_iva
                canon_oficial = projecte.canon_oficial
                if concedit == 0: # para evitar problemas con la division si es 0
                    percen_canon_oficial = 0.00
                else:
                    percen_canon_oficial = ((canon_oficial / concedit)*(100*(1+projecte.percen_iva/100)))
                #Calculamos el canon mas grande entre el del creaf y el oficial,para luego calcular el canon total
                if percen_canon_oficial > projecte.percen_canon_creaf:
                    canon_max = percen_canon_oficial
                else:
                    canon_max = projecte.percen_canon_creaf

                iva = (( concedit * percen_iva ) / (100*(1+percen_iva/100)))
                base_canon = concedit# Ojo que no es correct,o esto son los ingresos
                canon_creaf = (concedit*projecte.percen_canon_creaf)/(100*(1+projecte.percen_iva/100))
                canon_total = (concedit-iva) * (canon_max/100)
                # diferencia_per = (percen_canon_oficial-percen_canon_creaf)
                dif_canon = abs(canon_oficial - canon_creaf) # Ojo la funcion abs() sirve para ver la diferencia entre 2 numeros, evitando asi un resultado con -
                if base_canon != 0:
                    percen_1 = (canon_creaf/base_canon)*100
                    percen_2 = (canon_oficial/base_canon)*100
                else:
                    percen_1 = 0
                    percen_2 = 0

                if ingressos != 0:
                    percen_3 = (canon_aplicat/ingressos)*100
                else:
                    percen_3 = 0
                # net_disponible = concedit-iva-canon

                canon_pendent_aplicar = round(canon_creaf)-canon_aplicat
                saldo_canon_oficial = round(canon_oficial)-canon_aplicat
                #redondeamos para mostrar 2 decimales en los resultados

                base_canon = round(base_canon,2)
                percen_1 = round(percen_1,2)
                canon_creaf = round(canon_creaf,2)
                percen_2 = round(percen_2,2)
                canon_oficial = round(canon_oficial,2)
                percen_canon_oficial=round(percen_canon_oficial,2)
                dif_canon = round(dif_canon,2)
                ingressos = round(ingressos,2)
                percen_3 = round(percen_3,2)
                canon_aplicat = round(canon_aplicat,2)
                canon_pendent_aplicar = round(canon_pendent_aplicar,2)
                saldo_canon_oficial = round(saldo_canon_oficial,2)

                #############
                #Hora de ir sumando los resultados de cada proyecto del investigador
                proyectos.append({
                    "codi":codigo_entero,
                    "nom":projecte.acronim,
                    "base_canon":base_canon,
                    "percen_1":percen_1,
                    "canon_creaf":canon_creaf,
                    "percen_2":percen_2,
                    "canon_oficial":canon_oficial,
                    "percen_canon_oficial":percen_canon_oficial,
                    "dif_canon":dif_canon,
                    "ingressos":ingressos,
                    "percen_3":percen_3,
                    "canon_aplicat":canon_aplicat,
                    "canon_pendent_aplicar":canon_pendent_aplicar,
                    "saldo_canon_oficial":saldo_canon_oficial
                })

                #totales:
                total_base_canon = round(total_base_canon+base_canon,2)
                total_canon_creaf = round(total_canon_creaf+canon_creaf,2)
                total_canon_oficial = round(total_canon_oficial+canon_oficial,2)
                total_dif_canon = round(total_dif_canon+dif_canon,2)
                total_ingressos = round(total_ingressos+ingressos,2)
                total_canon_aplicat = round(total_canon_aplicat+canon_aplicat,2)
                total_canon_pendent_aplicar = round(total_canon_pendent_aplicar+canon_pendent_aplicar,2)
                total_saldo_canon_oficial = round(total_saldo_canon_oficial+saldo_canon_oficial,2)

                if total_base_canon !=0:
                    total_percen_1 = round((total_canon_creaf/total_base_canon)*100,2)
                    total_percen_2 = round((total_canon_oficial/total_base_canon)*100,2)
                else:
                    total_percen_1 = 0
                    total_percen_2 = 0

                if total_ingressos != 0:
                    total_percen_3 = round((total_canon_aplicat/total_ingressos)*100,2)
                else:
                    total_percen_3 = 0
                #

        #anadimos finalmente los totales al investigador,y este,al resultado
        #OJO estos calculos no son correctos,preguntar
        total_percen_1 = round(total_percen_1/num_investigadores,2)
        total_percen_2 = round(total_percen_2/num_investigadores,2)
        total_percen_3 = round(total_percen_3/num_investigadores,2)

        totals.append({
            "total_base_canon":total_base_canon,
            "total_percen_1":total_percen_1,
            "total_canon_creaf":total_canon_creaf,
            "total_percen_2":total_percen_2,
            "total_canon_oficial":total_canon_oficial,
            "total_dif_canon":total_dif_canon,
            "total_ingressos":total_ingressos,
            "total_percen_3":total_percen_3,
            "total_canon_aplicat":total_canon_aplicat,
            "total_canon_pendent_aplicar":total_canon_pendent_aplicar,
            "total_saldo_canon_oficial":total_saldo_canon_oficial
        })

        datos_inv.append({"nom_responsable":nom_resp,"data_max":fecha_max,"projectes":proyectos,"totals":totals})
        resultado.append(datos_inv)
        proyectos = []
        totals = []
        datos_inv = []


    return resultado

def ComptesNoAssignats(projectes):#Comptes NO assignats a cap projecte
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        comptes = []
        resultado = []
        lista_codigos = ""
        saldo=0
        total_carrec = 0
        total_ingressos = 0
        total_saldo = 0

        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp)
            ##### poner 0 en los codigos si son demasiado cortos para tener x tamano

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)

            codigo_entero=cod_responsable+cod_projecte
            lista_codigos=lista_codigos+codigo_entero

        # 105 en el convert equivale al dd-mm-yyyy
        cursor.execute("SELECT TOP 100 PERCENT Plan_cuentas.Cuenta, Plan_cuentas.Titulo, Sum(Apuntes.Debe) AS TotalDebe, Sum(Apuntes.Haber) AS TotalHaber FROM Plan_cuentas LEFT JOIN Apuntes ON (Plan_cuentas.Cuenta = Apuntes.Cuenta) WHERE ( (Plan_cuentas.Nivel=0) AND ((Plan_cuentas.Cuenta LIKE '7%%') OR (Plan_cuentas.Cuenta LIKE '6%%') OR (Plan_cuentas.Cuenta LIKE '2%%')) AND (Apuntes.Diario='0' OR Apuntes.Diario='4' OR Apuntes.Diario='1') AND (Apuntes.Fecha>=CONVERT(date,(?),105) AND Apuntes.Fecha<=CONVERT(date,(?),105)) AND ( RIGHT(Plan_cuentas.Cuenta, 5) NOT IN ((?)))) GROUP BY Plan_cuentas.Cuenta, Plan_cuentas.Titulo ORDER BY Plan_cuentas.Cuenta",[fecha_min,fecha_max,lista_codigos])
        projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve

        ##### Para ir restando el saldo pendiente a medida que salen ingresos:
        for prjfet in projectfetch:
            if prjfet["TotalHaber"] == None:
                prjfet["TotalHaber"] = 0
            if prjfet["TotalDebe"] == None:
                prjfet["TotalDebe"] = 0

            saldo=round((saldo-prjfet["TotalDebe"])+prjfet["TotalHaber"],2)
            prjfet["Saldo"]=saldo
            total_saldo=saldo
            total_carrec=total_carrec+prjfet["TotalHaber"]
            total_ingressos=total_ingressos+prjfet["TotalDebe"]



        resultado.append({"comptes":projectfetch,'data_min':fecha_min,'data_max':fecha_max,"total_carrec":total_carrec,"total_ingressos":total_ingressos,"total_saldo":total_saldo})

        return resultado
