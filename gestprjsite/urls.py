#from django.conf.urls import  include, url #patterns,
from django.views.generic import TemplateView
from django.contrib import admin
from gestprj import views
from rest_framework import routers
from django.conf import settings
#from django.conf.urls import include, url #patterns,
from django.urls import include, re_path


# Estos son necesarios para que funcione los serializers de cada uno
router = routers.DefaultRouter()
router.register(r'centresPart_rest',views.CentresParticipantsViewSet) #post crear put actualizar y delete eliminar
router.register(r'gestor_centresPart',views.GestCentresParticipants)

# router.register(r'TOrganismes_rest',views.ListTOrganismes)# todos los organismos
router.register(r'gestor_TOrganismes',views.GestTOrganismes)# gestionar organismos

router.register(r'gestor_UsuariCreaf',views.GestTUsuarisCreaf)# gestionar y mostrar los usuarios internos
router.register(r'gestor_PersonalCreaf',views.GestPersonalCreaf)# gestionar y mostrartodo el personal interno

router.register(r'gestor_UsuariExtern',views.GestTUsuarisExterns)# gestionar y mostrar los usuarios externos
router.register(r'gestor_PersonalExtern',views.GestPersonalExtern)# gestionar y mostrartodo el personal externo

router.register(r'gestor_UsuariXarxa',views.GestTUsuarisXarxa)# gestionar y mostrar los usuarios internos

router.register(r'gestor_Responsables',views.GestResponsables)# gestionar y mostrar los responsables

router.register(r'gestor_JustificPersonal',views.GestJustificPersonal)# gestionar justificaciones de personal creaf

router.register(r'gestor_OrganismesFin',views.GestOrganismesFin)# gestionar organismos financiadores
router.register(r'gestor_OrganismesRec',views.GestOrganismesRec)# gestionar organismos receptores

router.register(r'gestor_JustificInternes',views.GestJustifInternes)# gestionar justificaciones de personal creaf

router.register(r'gestor_Renovacions',views.GestRenovacions)# gestionar justificaciones de personal creaf

router.register(r'gestor_Pressupost',views.GestPressupost)

router.register(r'gestor_ConceptePressupostari',views.GestConceptesPress)

router.register(r'gestor_PeriodicitatPres',views.GestPeriodicitatPres)
router.register(r'gestor_PeriodicitatPartida',views.GestPeriodicitatPartida)

router.register(r'gestor_Desglossament',views.GestDesglossament)

router.register(r'gestor_JustificacionsProjecte',views.GestJustificacionsProjecte)
router.register(r'gestor_Auditories',views.GestAuditories)

router.register(r'gestor_CompromesPersonal',views.GestComprometidoPersonal)

router.register(r'gestor_PermisosUsuarisConsultar',views.GestPrjUsuaris)

router.register(r'gestor_GrupsPci',views.GestGrupsPci)
router.register(r'gestor_OrganismeGrupPci',views.GestOrganismeGrupPci)

router.register(r'projectes_rest',views.ProjectesViewSet)


urlpatterns = [#patterns('',
    # Examples:
    # url(r'^$', 'gestprjsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #re_path(r'^admin/', include(admin.site.urls)),
    #re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.index, name='index'),
    #re_path(r'^', include(router.urls)),
    re_path(r'^', include(router.urls)),
    re_path('^show_centresPart/(?P<id_projecte>.+)/$', views.ListCentresParticipantsProjecte.as_view()),
    re_path('^show_TOrganismes/(?P<id_projecte>.+)/$', views.ListTOrganismesNoProjecte.as_view()),# organismos que no estan en el proyecto
    # AJAX selects:
    re_path('^llista_organismes_select/', views.ListOrganismesSelect),# para los select con el nombre de los organismos
    re_path('^llista_projectes_select/', views.ListProjectesSelect),# para el select con los proyectos
    re_path('^llista_usuaris_creaf_select/', views.ListUsuarisCreafSelect),# para el select con los usuarios
    re_path('^llista_usuaris_xarxa_select/', views.ListUsuarisXarxaSelect),# para el select con los usuarios de red
    re_path('^llista_usuaris_externs_select/', views.ListUsuarisExternsSelect),# para el select con los usuarios en coordinat per altres
    re_path('^llista_responsables_select/', views.ListResponsablesSelect),# para el select con los usuarios de red
    re_path('^llista_grups_pci_select/', views.ListGrupsPciSelect),# para los select con el nombre de los organismos

    re_path('^llista_Organismes/', views.ListTOrganismes.as_view()),# para la datatable de organismes cabecera
    re_path('^llista_Usuaris_creaf/', views.ListUsuarisCreaf.as_view()),# para la datatable de personal creaf cabecera
    re_path('^llista_Usuaris_externs/', views.ListUsuarisExterns.as_view()),# para la datatable de personal extern cabecera
    re_path('^llista_Usuaris_xarxa/', views.ListUsuarisXarxa.as_view()),# para la datatable de usuaris xarxa cabecera
    re_path('^llista_Responsables/', views.ListResponsables.as_view()),# para la datatable de responsables cabecera
    re_path('^llista_permisos_usuaris_consultar/', views.ListPermisosUsuarisConsultar.as_view()),# para la datatable de permisos usuaris cabecera
    re_path('^llista_ConceptesPres/', views.ListConceptesPress),# para los select con el nombre de las partidas
    re_path('^llista_justificacions_cabecera/(?P<fecha_min>.+)/(?P<fecha_max>.+)/$', views.ListJustificacionsCabecera),# justificaciones en edicio en la cabecera
    re_path('^generar_informe_periode_cabecera/$', views.GenerarInformePeriode),
    re_path('^generar_informe_financadors_periode_cabecera/$', views.GenerarInformeFinancadorsPeriode),
    re_path('^generar_informe_receptors_periode_cabecera/$', views.GenerarInformeReceptorsPeriode),
    re_path('^generar_informe_justificacions_internes_periode_cabecera/$', views.GenerarInformeJustificacionsInternesPeriode),
    re_path('^generar_informe_concessions_periode_cabecera/$', views.GenerarInformeConcessionsPeriode),
    re_path('^llista_projectes_responsable_consultar/', views.ListProjectesResponsableCabecera),# para la cabecera
    re_path('^llista_pci_consultar/(?P<id_grup>.+)/(?P<fecha_min_pci>.+)/(?P<fecha_max_pci>.+)/$', views.ListPciCabecera),# para la cabecera
    re_path('^llista_grups_pci_consultar/', views.ListGrupsPci.as_view()),# para la datatable de grups pci cabecera
    re_path('^llista_organismes_grup_pci/(?P<id_grup>.+)/$', views.ListOrganismesGrupPci.as_view()),# para la cabecera
    re_path('^afegir_organisme_grup_pci/', views.AfegirOrganismeGrupPci),# para la cabecera
    re_path('^llista_usuaris_xarxa_sense_assignar/', views.ListUsuarisXarxaSenseAssignar),# para la cabecera
    re_path('^afegir_usuari_xarxa_sense_assignar/', views.AfegirUsuarisXarxaSenseAssignar),# para la cabecera

    re_path('^show_Personal_creaf/(?P<id_projecte>.+)/$', views.ListPersonalCreafNoProjecte.as_view()),# personal itnerno que no este en el proyecto
    re_path('^show_Personal_creaf_prj/(?P<id_projecte>.+)/$', views.ListPersonalCreafProjecte.as_view()),# personal interno de un proyecto


    re_path('^show_Personal_extern/(?P<id_projecte>.+)/$', views.ListPersonalExternNoProjecte.as_view()),# personal externo que no este en el proyecto
    re_path('^show_Personal_extern_prj/(?P<id_projecte>.+)/$', views.ListPersonalExternProjecte.as_view()),# personal externo de un proyecto

    re_path('^show_justificPersonal/(?P<id_personal>.+)/$', views.ListJustificPersonal.as_view()),# justificaciones de el usuario de creaf especificado

    re_path('^show_OrganismesFin/(?P<id_projecte>.+)/$', views.ListOrganismesFin.as_view()),# organismos que financian a x proyercto

    re_path('^show_OrganismesRec/(?P<id_projecte>.+)/$', views.ListOrganismesRec.as_view()),# organismos que reciben de x proyercto

    re_path('^show_justificInternes/(?P<id_projecte>.+)/$', views.ListJustifInternes.as_view()),# organismos que reciben de x proyercto

    re_path('^show_Renovacions/(?P<id_projecte>.+)/$', views.ListRenovacions.as_view()),# organismos que reciben de x proyercto

    re_path('^show_Pressupost/(?P<id_projecte>.+)/$', views.ListPressupost.as_view()),


    re_path('^show_PeriodicitatPres/(?P<id_projecte>.+)/$', views.ListPeriodicitatPres.as_view()),
    re_path('^show_PeriodicitatPartida/(?P<id_partida>.+)/$', views.ListPeriodicitatPartida.as_view()),

    re_path('^show_Desglossament/(?P<id_partida>.+)/$', views.ListDesglossament.as_view()),

    re_path('^show_JustificacionsProjecte/(?P<id_projecte>.+)/$', views.ListJustificacionsProjecte.as_view()),

    re_path('^show_Auditories/(?P<id_projecte>.+)/$', views.ListAuditories.as_view()),

    #JSON
    # re_path(r'^show_compromes/(?P<id_projecte>.+)/$', views.ListCompromes, name="compromes"),
    re_path(r'^show_compromes_personal/(?P<id_projecte>.+)/$', views.ListCompromesPersonal.as_view(), name="compromesPersonal"),
    # re_path(r'^show_compromes_partida/(?P<id_partida>.+)/(?P<id_projecte>.+)/$', views.ListCompromesPartida, name="compromes_partida"),

    # re_path('^show_compromes_compte/(?P<id_compte>.+)/$', views.ListCompromesCompte.as_view()),


    re_path(r'^llista_projectes/', views.list_projectes, name='llista_projectes'),
    # re_path(r'^projecte_nou/(?P<id>.+)/$', views.new_project, name='projecte_nou'),
    # re_path(r'^projecte_nou/', views.new_project, name='projecte_nou'),
    re_path(r'^modificar_projecte/(?P<id>.+)/$', views.mod_project, name='modificar_projecte'), # Muy importante el orden en el que estan colocadas esta linea y la de abajo!!!
    re_path(r'^modificar_projecte/', views.mod_project, name='modificar_projecte'),
    re_path(r'^login/', views.login_view, name='login'),
    re_path(r'^logout/', views.logout_view, name='logout'),
    re_path(r'^welcome/$', TemplateView.as_view(template_name="gestprj/welcome.html"), name='welcome'),
    re_path(r'^thanks/$', TemplateView.as_view(template_name="gestprj/thanks.html"), name='thanks'),
    re_path(r'^menu/$', TemplateView.as_view(template_name="gestprj/menu.html"), name='menu'),

    re_path(r'^comptabilitat/$', views.list_projectes_cont, name='comptabilitat'),
    re_path(r'^json_vacio/$', views.json_vacio, name='cont_json_vacio'),
    re_path(r'^json_vacio_results/$', views.json_vacio_results, name='json vacio pero para datasrc results'),
    re_path(r'^cont_dades/$', views.cont_dades, name='cont_dades'),

    re_path(r'^cont_estat_pres/$', views.cont_estat_pres, name='cont_estat_pres'),
    re_path(r'^show_estat_pres_datos/(?P<datos>.+)/$', views.ListEstatPresDatos, name='cont_estat_pres_datos'),# ajax 1
    re_path(r'^show_Despeses_Compte/(?P<id_partida>.+)/(?P<cod>.+)/(?P<data_min>.+)/(?P<data_max>.+)/$', views.ListDespesesCompte, name="despeses_compte"),# ajax 2

    re_path(r'^cont_despeses/$', views.cont_despeses, name='cont_despeses'),
    re_path(r'^cont_despeses_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$', views.ListDespesesDatos, name='cont_despeses_datos'),# ajax 1

    re_path(r'^cont_ingresos/$', views.cont_ingresos, name='cont_ingresos'),
    re_path(r'^cont_ingresos_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$', views.ListIngresosDatos, name='cont_ingresos_datos'),# ajax 1

    re_path(r'^cont_estat_prj_resp/$', views.cont_estat_prj_resp, name='estat_prj_resp'),
    re_path(r'^show_estat_prj_resp_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<proyectos>.+)/$', views.ListEstatPrjRespDatos, name='estat_prj_resp_datos'),# ajax 1

    re_path(r'^cont_resum_fitxa_major_prj/$', views.cont_resum_fitxa_major_prj, name='resum_fitxa_major_prj'),
    re_path(r'^show_resum_fitxa_major_prj_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$', views.ListResumFitxaMajorPrjDatos, name='resum_fitxa_major_prj_datos'),# ajax 1
    #moviments compte
    re_path(r'^show_Moviments_Compte/(?P<compte>.+)/(?P<data_min>.+)/(?P<data_max>.+)/$', views.ListMovimentsCompte, name="moviments_compte"), # ajax2

    re_path(r'^cont_resum_estat_prj/$', views.cont_resum_estat_prj, name='resum_estat_prj'),
    re_path(r'^cont_resum_estat_canon/$', views.cont_resum_estat_canon, name='resum_estat_canon'),
    re_path(r'^show_resum_estat_canon_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$',views.ListResumEstatCanonDatos, name='resum_estat_canon_datos'),  # ajax 1

    re_path(r'^cont_fitxa_major_prj/$', views.cont_fitxa_major_prj, name='fitxa_major_prj'),
    re_path(r'^show_fitxa_major_prj_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$', views.ListFitxaMajorPrjDatos, name='fitxa_major_prj_datos'), # ajax1

    re_path(r'^cont_comptes_no_assignats/$', views.cont_comptes_no_assignats, name='comptes_no_assignats'),

    # IMPRIMIR LISTADOS EN CONTABILIDAD
    re_path(r'^imprimir_resum_estat_prj_resp/$', views.imprimir_resum_estat_prj_resp, name='estat_prj_resp_imprimir'),


    # JSON de contabilidad
    re_path(r'^show_ResponsablesCont/$', views.ListResponsablesCont, name="responsables llista"),
    re_path(r'^show_ProjectesCont/$', views.ListProjectesCont, name="projectes llista"),
    re_path(r'^show_compromes_projecte/(?P<id_projecte>.+)/(?P<codigo_entero>.+)/$', views.ListCompromesProjecte, name="Compromes Projecte"),
    re_path(r'^show_compromes_compte/(?P<tipo_comp>.+)/(?P<id_projecte>.+)/(?P<codigo>.+)/(?P<compte>.+)/$', views.ListCompromesCompte, name="Compromes Compte de Projecte"),
    re_path(r'^show_compromes_llista_comptes/(?P<id_projecte>.+)/(?P<codigo_entero>.+)/(?P<llista_comptes>.+)/$', views.ListCompromesLlistaComptes, name="Compromes Llista Comptes de Projecte"),

    re_path(r'^show_lineas_albaran/(?P<id_albaran>.+)/$', views.LineasAlbaran, name="Lineas albaran"),
    re_path(r'^show_lineas_pedido/(?P<id_pedido>.+)/$', views.LineasPedido, name="Lineas pedido"),
    re_path(r'^show_lineas_pedido_detalles/(?P<num_apunte>.+)/$', views.LineasPedidoDetalles, name="Lineas pedido detalles"),

    # url(r'^show_compromes_partida/(?P<id_projecte>.+)/(?P<partida>.+)/$', views.ListCompromesPartida, name="Compromes Partida de Projecte"),
    #
]#)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )