from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from gestprj import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls import include, patterns, url


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

router.register(r'projectes_rest',views.ProjectesViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gestprjsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^', include(router.urls)),
    url('^show_centresPart/(?P<id_projecte>.+)/$', views.ListCentresParticipantsProjecte.as_view()),
    url('^show_TOrganismes/(?P<id_projecte>.+)/$', views.ListTOrganismesNoProjecte.as_view()),# organismos que no estan en el proyecto
    # AJAX selects:
    url('^llista_organismes_select/', views.ListOrganismesSelect),# para los select con el nombre de los organismos
    url('^llista_projectes_select/', views.ListProjectesSelect),# para el select con los proyectos
    url('^llista_usuaris_creaf_select/', views.ListUsuarisCreafSelect),# para el select con los usuarios
    url('^llista_usuaris_xarxa_select/', views.ListUsuarisXarxaSelect),# para el select con los usuarios de red
    url('^llista_usuaris_externs_select/', views.ListUsuarisExternsSelect),# para el select con los usuarios en coordinat per altres
    url('^llista_responsables_select/', views.ListResponsablesSelect),# para el select con los usuarios de red

    url('^llista_Organismes/', views.ListTOrganismes.as_view()),# para la datatable de organismes cabecera
    url('^llista_Usuaris_creaf/', views.ListUsuarisCreaf.as_view()),# para la datatable de personal creaf cabecera
    url('^llista_Usuaris_externs/', views.ListUsuarisExterns.as_view()),# para la datatable de personal extern cabecera
    url('^llista_Usuaris_xarxa/', views.ListUsuarisXarxa.as_view()),# para la datatable de usuaris xarxa cabecera
    url('^llista_Responsables/', views.ListResponsables.as_view()),# para la datatable de responsables cabecera
    url('^llista_permisos_usuaris_consultar/', views.ListPermisosUsuarisConsultar.as_view()),# para la datatable de permisos usuaris cabecera
    url('^llista_ConceptesPres/', views.ListConceptesPress),# para los select con el nombre de las partidas
    url('^llista_justificacions_cabecera/(?P<fecha_min>.+)/(?P<fecha_max>.+)/$', views.ListJustificacionsCabecera),# justificaciones en edicio en la cabecera
    url('^llista_projectes_responsable_consultar/', views.ListProjectesResponsableCabecera),# para la cabecera
    url('^llista_pci_consultar/(?P<id_organisme>.+)/$', views.ListPciCabecera),# para la cabecera
    url('^llista_usuaris_xarxa_sense_assignar/', views.ListUsuarisXarxaSenseAssignar),# para la cabecera
    url('^afegir_usuari_xarxa_sense_assignar/', views.AfegirUsuarisXarxaSenseAssignar),# para la cabecera

    url('^show_Personal_creaf/(?P<id_projecte>.+)/$', views.ListPersonalCreafNoProjecte.as_view()),# personal itnerno que no este en el proyecto
    url('^show_Personal_creaf_prj/(?P<id_projecte>.+)/$', views.ListPersonalCreafProjecte.as_view()),# personal interno de un proyecto


    url('^show_Personal_extern/(?P<id_projecte>.+)/$', views.ListPersonalExternNoProjecte.as_view()),# personal externo que no este en el proyecto
    url('^show_Personal_extern_prj/(?P<id_projecte>.+)/$', views.ListPersonalExternProjecte.as_view()),# personal externo de un proyecto

    url('^show_justificPersonal/(?P<id_personal>.+)/$', views.ListJustificPersonal.as_view()),# justificaciones de el usuario de creaf especificado

    url('^show_OrganismesFin/(?P<id_projecte>.+)/$', views.ListOrganismesFin.as_view()),# organismos que financian a x proyercto

    url('^show_OrganismesRec/(?P<id_projecte>.+)/$', views.ListOrganismesRec.as_view()),# organismos que reciben de x proyercto

    url('^show_justificInternes/(?P<id_projecte>.+)/$', views.ListJustifInternes.as_view()),# organismos que reciben de x proyercto

    url('^show_Renovacions/(?P<id_projecte>.+)/$', views.ListRenovacions.as_view()),# organismos que reciben de x proyercto

    url('^show_Pressupost/(?P<id_projecte>.+)/$', views.ListPressupost.as_view()),


    url('^show_PeriodicitatPres/(?P<id_projecte>.+)/$', views.ListPeriodicitatPres.as_view()),
    url('^show_PeriodicitatPartida/(?P<id_partida>.+)/$', views.ListPeriodicitatPartida.as_view()),

    url('^show_Desglossament/(?P<id_partida>.+)/$', views.ListDesglossament.as_view()),

    url('^show_JustificacionsProjecte/(?P<id_projecte>.+)/$', views.ListJustificacionsProjecte.as_view()),

    url('^show_Auditories/(?P<id_projecte>.+)/$', views.ListAuditories.as_view()),

    #JSON
    # url(r'^show_compromes/(?P<id_projecte>.+)/$', views.ListCompromes, name="compromes"),
    url(r'^show_compromes_personal/(?P<id_projecte>.+)/$', views.ListCompromesPersonal.as_view(), name="compromesPersonal"),
    # url(r'^show_compromes_partida/(?P<id_partida>.+)/(?P<id_projecte>.+)/$', views.ListCompromesPartida, name="compromes_partida"),

    # url('^show_compromes_compte/(?P<id_compte>.+)/$', views.ListCompromesCompte.as_view()),


    url(r'^llista_projectes/', views.list_projectes, name='llista_projectes'),
    # url(r'^projecte_nou/(?P<id>.+)/$', views.new_project, name='projecte_nou'),
    # url(r'^projecte_nou/', views.new_project, name='projecte_nou'),
    url(r'^modificar_projecte/(?P<id>.+)/$', views.mod_project, name='modificar_projecte'), # Muy importante el orden en el que estan colocadas esta linea y la de abajo!!!
    url(r'^modificar_projecte/', views.mod_project, name='modificar_projecte'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^welcome/$', TemplateView.as_view(template_name="gestprj/welcome.html"), name='welcome'),
    url(r'^thanks/$', TemplateView.as_view(template_name="gestprj/thanks.html"), name='thanks'),
    url(r'^menu/$', TemplateView.as_view(template_name="gestprj/menu.html"), name='menu'),

    url(r'^contabilitat/$', views.list_projectes_cont, name='contabilitat'),
    url(r'^json_vacio/$', views.json_vacio, name='cont_json_vacio'),
    url(r'^json_vacio_results/$', views.json_vacio_results, name='json vacio pero para datasrc results'),
    url(r'^cont_dades/$', views.cont_dades, name='cont_dades'),

    url(r'^cont_estat_pres/$', views.cont_estat_pres, name='cont_estat_pres'),
    url(r'^show_estat_pres_datos/(?P<datos>.+)/$', views.ListEstatPresDatos, name='cont_estat_pres_datos'),# ajax 1
    url(r'^show_Despeses_Compte/(?P<id_partida>.+)/(?P<cod>.+)/(?P<data_min>.+)/(?P<data_max>.+)/$', views.ListDespesesCompte, name="despeses_compte"),# ajax 2

    url(r'^cont_despeses/$', views.cont_despeses, name='cont_despeses'),
    url(r'^cont_despeses_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$', views.ListDespesesDatos, name='cont_despeses_datos'),# ajax 1

    url(r'^cont_ingresos/$', views.cont_ingresos, name='cont_ingresos'),
    url(r'^cont_ingresos_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$', views.ListIngresosDatos, name='cont_ingresos_datos'),# ajax 1

    url(r'^cont_estat_prj_resp/$', views.cont_estat_prj_resp, name='estat_prj_resp'),
    url(r'^show_estat_prj_resp_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<proyectos>.+)/$', views.ListEstatPrjRespDatos, name='estat_prj_resp_datos'),# ajax 1

    url(r'^cont_resum_fitxa_major_prj/$', views.cont_resum_fitxa_major_prj, name='resum_fitxa_major_prj'),
    url(r'^show_resum_fitxa_major_prj_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$', views.ListResumFitxaMajorPrjDatos, name='resum_fitxa_major_prj_datos'),# ajax 1
    #moviments compte
    url(r'^show_Moviments_Compte/(?P<compte>.+)/(?P<data_min>.+)/(?P<data_max>.+)/$', views.ListMovimentsCompte, name="moviments_compte"), # ajax2

    url(r'^cont_resum_estat_prj/$', views.cont_resum_estat_prj, name='resum_estat_prj'),
    url(r'^cont_resum_estat_canon/$', views.cont_resum_estat_canon, name='resum_estat_canon'),
    url(r'^show_resum_estat_canon_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$',views.ListResumEstatCanonDatos, name='resum_estat_canon_datos'),  # ajax 1

    url(r'^cont_fitxa_major_prj/$', views.cont_fitxa_major_prj, name='fitxa_major_prj'),
    url(r'^show_fitxa_major_prj_datos/(?P<fecha_min>.+)/(?P<fecha_max>.+)/(?P<codigo>.+)/$', views.ListFitxaMajorPrjDatos, name='fitxa_major_prj_datos'), # ajax1

    url(r'^cont_comptes_no_assignats/$', views.cont_comptes_no_assignats, name='comptes_no_assignats'),

    # IMPRIMIR LISTADOS EN CONTABILIDAD
    url(r'^imprimir_resum_estat_prj_resp/$', views.imprimir_resum_estat_prj_resp, name='estat_prj_resp_imprimir'),


    # JSON de contabilidad
    url(r'^show_ResponsablesCont/$', views.ListResponsablesCont, name="responsables llista"),
    url(r'^show_ProjectesCont/$', views.ListProjectesCont, name="projectes llista"),
    url(r'^show_compromes_projecte/(?P<id_projecte>.+)/(?P<codigo_entero>.+)/$', views.ListCompromesProjecte, name="Compromes Projecte"),
    url(r'^show_compromes_compte/(?P<tipo_comp>.+)/(?P<id_projecte>.+)/(?P<codigo>.+)/(?P<compte>.+)/$', views.ListCompromesCompte, name="Compromes Compte de Projecte"),
    url(r'^show_compromes_llista_comptes/(?P<id_projecte>.+)/(?P<codigo_entero>.+)/(?P<llista_comptes>.+)/$', views.ListCompromesLlistaComptes, name="Compromes Llista Comptes de Projecte"),

    url(r'^show_lineas_albaran/(?P<id_albaran>.+)/$', views.LineasAlbaran, name="Lineas albaran"),
    url(r'^show_lineas_pedido/(?P<id_pedido>.+)/$', views.LineasPedido, name="Lineas pedido"),
    url(r'^show_lineas_pedido_detalles/(?P<num_apunte>.+)/$', views.LineasPedidoDetalles, name="Lineas pedido detalles"),

    # url(r'^show_compromes_partida/(?P<id_projecte>.+)/(?P<partida>.+)/$', views.ListCompromesPartida, name="Compromes Partida de Projecte"),
    #
)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )